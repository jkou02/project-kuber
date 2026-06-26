"""Modelo de transacción (fuente de verdad)."""

import enum
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin, int_pk


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    payment_method_id: Mapped[int] = mapped_column(
        ForeignKey("payment_methods.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    income_source_id: Mapped[int | None] = mapped_column(
        ForeignKey("income_sources.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    type: Mapped[TransactionType] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="VES", nullable=False)
    exchange_rate: Mapped[float | None] = mapped_column(
        Numeric(20, 10),
        nullable=True,
    )
    amount_local_currency: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")
    payment_method: Mapped["PaymentMethod"] = relationship(
        back_populates="transactions",
    )
    income_source: Mapped["IncomeSource | None"] = relationship(
        back_populates="transactions",
    )
