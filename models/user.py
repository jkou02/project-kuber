"""Modelo de usuario."""

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin, int_pk


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )
    username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    default_currency: Mapped[str] = mapped_column(
        String(3),
        default="VES",
        nullable=False,
    )

    # Relaciones
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )
    categories: Mapped[list["Category"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )
    payment_methods: Mapped[list["PaymentMethod"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )
    income_sources: Mapped[list["IncomeSource"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )
    monthly_budgets: Mapped[list["MonthlyBudget"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )
