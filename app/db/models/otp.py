from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OTPRequest(Base):
    __tablename__ = "otp_requests"

    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    # is_used turns True once a verify call consumes this OTP request
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<OTPRequest id={self.id} email={self.email} is_used={self.is_used}>"
