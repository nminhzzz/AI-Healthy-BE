from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.models.payment import Payment, PaymentProvider, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter()

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Khởi tạo giao dịch thanh toán trực tuyến và lấy link thanh toán giả lập."""
    order = db.query(Order).filter(Order.id == payment_in.order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn hàng."
        )
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thanh toán cho đơn hàng này."
        )

    # Khởi tạo bản ghi thanh toán
    db_payment = Payment(
        order_id=order.id,
        provider=payment_in.provider,
        amount=order.total_price,
        status=PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    # Tạo URL thanh toán giả lập hướng tới cổng VNPAY Mockup
    # Khi user click Link này sẽ dẫn tới trang cổng giả lập để chọn thanh toán thành công hay thất bại
    payment_url = (
        f"http://localhost:3000/payment-result"
        f"?order_code={order.order_code}"
        f"&payment_id={db_payment.id}"
        f"&amount={order.total_price}"
        f"&provider={payment_in.provider}"
    )

    response = PaymentResponse.model_validate(db_payment)
    response.payment_url = payment_url
    return response

@router.get("/callback")
def payment_callback(
    order_code: str,
    payment_id: int,
    status_str: str,  # "success" hoặc "failed"
    db: Session = Depends(get_db)
):
    """Cổng thanh toán gọi callback (IPN) về máy chủ để cập nhật kết quả đặt hàng."""
    order = db.query(Order).filter(Order.order_code == order_code).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng tương ứng.")

    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch thanh toán.")

    if status_str == "success":
        payment.status = PaymentStatus.SUCCESS
        payment.paid_at = datetime.now()
        payment.transaction_id = f"MOCK-TXN-{payment.provider.value}-{int(datetime.now().timestamp())}"
        order.status = OrderStatus.PAID
    else:
        payment.status = PaymentStatus.FAILED
        # Giữ nguyên đơn hàng ở PENDING để người dùng có thể thử thanh toán lại

    db.commit()
    db.refresh(order)
    db.refresh(payment)

    return {
        "message": "Đã cập nhật trạng thái thanh toán đơn hàng thành công.",
        "order_code": order.order_code,
        "order_status": order.status.value,
        "payment_status": payment.status.value
    }
