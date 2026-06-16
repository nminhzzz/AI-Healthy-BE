"""
core/exceptions.py — Custom exceptions cho toàn bộ HealthShop AI backend.

Tất cả exception được kế thừa từ AppException (base class).
FastAPI sẽ bắt và chuyển thành HTTP response thông qua exception_handler middleware.
"""

from typing import Any


class AppException(Exception):
    """Base exception cho tất cả lỗi trong ứng dụng."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "Đã có lỗi xảy ra, vui lòng thử lại."

    def __init__(
        self,
        message: str | None = None,
        detail: Any = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.detail = detail
        super().__init__(self.message)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"status={self.status_code} "
            f"code={self.error_code!r} "
            f"message={self.message!r}>"
        )


# ── 400 Bad Request ───────────────────────────────────────────────────────────

class BadRequestException(AppException):
    status_code = 400
    error_code = "BAD_REQUEST"
    message = "Yêu cầu không hợp lệ."


class ValidationException(AppException):
    status_code = 422
    error_code = "VALIDATION_ERROR"
    message = "Dữ liệu không hợp lệ."


# ── 401 Unauthorized ──────────────────────────────────────────────────────────

class UnauthorizedException(AppException):
    status_code = 401
    error_code = "UNAUTHORIZED"
    message = "Bạn chưa đăng nhập hoặc token không hợp lệ."


class InvalidTokenException(AppException):
    status_code = 401
    error_code = "INVALID_TOKEN"
    message = "Token không hợp lệ hoặc đã hết hạn."


class InvalidCredentialsException(AppException):
    status_code = 401
    error_code = "INVALID_CREDENTIALS"
    message = "Email hoặc mật khẩu không đúng."


# ── 403 Forbidden ─────────────────────────────────────────────────────────────

class ForbiddenException(AppException):
    status_code = 403
    error_code = "FORBIDDEN"
    message = "Bạn không có quyền thực hiện hành động này."


# ── 404 Not Found ─────────────────────────────────────────────────────────────

class NotFoundException(AppException):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Không tìm thấy tài nguyên yêu cầu."


class UserNotFoundException(NotFoundException):
    error_code = "USER_NOT_FOUND"
    message = "Không tìm thấy người dùng."


class ProductNotFoundException(NotFoundException):
    error_code = "PRODUCT_NOT_FOUND"
    message = "Không tìm thấy sản phẩm."


class OrderNotFoundException(NotFoundException):
    error_code = "ORDER_NOT_FOUND"
    message = "Không tìm thấy đơn hàng."


class CategoryNotFoundException(NotFoundException):
    error_code = "CATEGORY_NOT_FOUND"
    message = "Không tìm thấy danh mục."


# ── 409 Conflict ──────────────────────────────────────────────────────────────

class ConflictException(AppException):
    status_code = 409
    error_code = "CONFLICT"
    message = "Dữ liệu đã tồn tại."


class EmailAlreadyExistsException(ConflictException):
    error_code = "EMAIL_EXISTS"
    message = "Email này đã được đăng ký."


# ── 422 Business Logic ────────────────────────────────────────────────────────

class InsufficientStockException(AppException):
    status_code = 422
    error_code = "INSUFFICIENT_STOCK"
    message = "Sản phẩm không đủ hàng trong kho."


class AccountInactiveException(AppException):
    status_code = 403
    error_code = "ACCOUNT_INACTIVE"
    message = "Tài khoản đã bị vô hiệu hóa."


# ── 500 Server Error ──────────────────────────────────────────────────────────

class DatabaseException(AppException):
    status_code = 500
    error_code = "DATABASE_ERROR"
    message = "Lỗi kết nối cơ sở dữ liệu."
