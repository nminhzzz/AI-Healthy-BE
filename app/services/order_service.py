import random
import string
from datetime import datetime
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from fastapi import HTTPException, status

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.coupon import Coupon
from app.repositories.cart_repo import cart_repo
from app.repositories.order_repo import order_repo
from app.schemas.order import OrderCreate

class OrderService:
    def _generate_order_code(self) -> str:
        """Tạo mã đơn hàng ngẫu nhiên duy nhất (Ví dụ: ORD-20260617-A8C3F)."""
        date_str = datetime.now().strftime("%Y%m%d")
        rand_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"ORD-{date_str}-{rand_suffix}"

    async def create_order(self, db: Session, redis_client: Redis, user_id: int, order_in: OrderCreate) -> Order:
        """Khởi tạo đơn hàng từ giỏ hàng trong Redis (chạy trong transaction của MySQL)."""
        raw_items = await cart_repo.get_cart_items(redis_client, user_id)
        if not raw_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Giỏ hàng trống. Không thể tiến hành thanh toán đặt hàng."
            )

        subtotal = 0.0
        order_items_to_create = []

        # Khởi đầu transaction
        try:
            # 1. Duyệt qua từng sản phẩm trong giỏ hàng và kiểm tra tồn kho
            for p_id_str, qty_str in raw_items.items():
                product_id = int(p_id_str)
                quantity = int(qty_str)

                # Sử dụng with_for_update() để khóa dòng sản phẩm, tránh tranh chấp tồn kho khi mua đồng thời
                product = db.query(Product).filter(Product.id == product_id).with_for_update().first()
                
                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Sản phẩm ID {product_id} không tồn tại."
                    )
                if not product.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Sản phẩm {product.name} đã ngừng kinh doanh."
                    )
                if product.stock < quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Sản phẩm {product.name} không đủ hàng trong kho (Còn lại: {product.stock})."
                    )

                # Tính toán giá tiền
                price = product.sale_price if product.sale_price is not None else product.price
                item_total = float(price) * quantity
                subtotal += item_total

                # Chuẩn bị thông tin dòng OrderItem
                order_items_to_create.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": float(price),
                    "total_price": item_total
                })

            # 2. Áp dụng mã giảm giá (nếu có)
            discount_amount = 0.0
            if order_in.coupon_id:
                coupon = db.query(Coupon).filter(Coupon.id == order_in.coupon_id, Coupon.is_active == True).first()
                if coupon:
                    # Kiểm tra ngày hết hạn
                    if coupon.expires_at is None or coupon.expires_at > datetime.now():
                        discount_amount = float(coupon.discount_amount)

            # 3. Tính phí vận chuyển (Miễn phí ship cho đơn từ 500.000đ, ngược lại 30.000đ)
            shipping_fee = 0.0 if subtotal >= 500000.0 else 30000.0
            total_price = subtotal - discount_amount + shipping_fee
            if total_price < 0.0:
                total_price = 0.0

            # 4. Tạo bản ghi Order
            order_code = self._generate_order_code()
            db_order = Order(
                user_id=user_id,
                coupon_id=order_in.coupon_id,
                order_code=order_code,
                subtotal=subtotal,
                discount_amount=discount_amount,
                shipping_fee=shipping_fee,
                total_price=total_price,
                receiver_name=order_in.receiver_name,
                phone=order_in.phone,
                province=order_in.province,
                district=order_in.district,
                ward=order_in.ward,
                address_detail=order_in.address_detail,
                payment_method=order_in.payment_method,
                status=OrderStatus.PENDING,
                note=order_in.note
            )
            db.add(db_order)
            db.flush()  # Lấy ID của order vừa tạo

            # 5. Tạo các dòng OrderItem và cập nhật tồn kho MySQL
            for item in order_items_to_create:
                prod = item["product"]
                qty = item["quantity"]

                # Lưu chi tiết sản phẩm đơn hàng
                db_item = OrderItem(
                    order_id=db_order.id,
                    product_id=prod.id,
                    product_name=prod.name,
                    quantity=qty,
                    unit_price=item["unit_price"],
                    total_price=item["total_price"]
                )
                db.add(db_item)
                
                # Trừ tồn kho
                prod.stock -= qty

            # 6. Commit transaction để lưu vĩnh viễn vào DB
            db.commit()
            db.refresh(db_order)

            # 7. Xóa sạch giỏ hàng trên Redis sau khi đặt hàng thành công
            await cart_repo.clear_cart(redis_client, user_id)
            return db_order

        except Exception as e:
            db.rollback()
            raise e

    def get_order_detail(self, db: Session, user_id: int, order_id: int) -> Order:
        """Lấy thông tin chi tiết đơn hàng của người dùng."""
        order = order_repo.get(db, id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")
        if order.user_id != user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xem đơn hàng này.")
        return order

    def cancel_order(self, db: Session, user_id: int, order_id: int) -> Order:
        """Hủy đơn hàng nếu đơn ở trạng thái PENDING và hoàn trả lại số lượng tồn kho."""
        order = order_repo.get(db, id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")
        if order.user_id != user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền hủy đơn hàng này.")
        if order.status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chỉ có thể hủy đơn hàng đang ở trạng thái chờ duyệt (PENDING)."
            )

        try:
            # Hoàn trả lại tồn kho sản phẩm
            for item in order.items:
                product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
                if product:
                    product.stock += item.quantity
            
            # Cập nhật trạng thái
            order.status = OrderStatus.CANCELLED
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise e

    def admin_update_order_status(self, db: Session, order_id: int, new_status: OrderStatus) -> Order:
        """Cập nhật trạng thái đơn hàng bởi Admin (xử lý hoàn trả tồn kho nếu hủy đơn)."""
        order = order_repo.get(db, id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")
        
        if order.status == new_status:
            return order
            
        # Không cho phép chuyển trạng thái nếu đã hoàn thành hoặc đã hủy
        if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Không thể thay đổi trạng thái của đơn hàng đã {order.status.value}."
            )
            
        try:
            # Nếu chuyển sang trạng thái CANCELLED, hoàn trả tồn kho
            if new_status == OrderStatus.CANCELLED:
                for item in order.items:
                    product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
                    if product:
                        product.stock += item.quantity
            
            # Cập nhật trạng thái mới
            order.status = new_status
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise e

order_service = OrderService()

