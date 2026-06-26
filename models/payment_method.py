"""Modelo de método de pago."""

import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin, int_pk


class PaymentMethodType(str, enum.Enum):
    CASH = "cash"
    BANK = "bank"
    MOBILE = "mobile"
    CRYPTO = "crypto"
    OTHER = "other"


class PaymentMethod(Base, TimestampMixin):
    __tablename__ = "payment_methods"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[PaymentMethodType] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="VES", nullable=False)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="payment_methods")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="payment_method",
        lazy="selectin",
    )
