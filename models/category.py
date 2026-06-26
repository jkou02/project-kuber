"""Modelo de categoría de transacción."""

import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin, int_pk


class CategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[CategoryType] = mapped_column(nullable=False)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category",
        lazy="selectin",
    )
    monthly_budgets: Mapped[list["MonthlyBudget"]] = relationship(
        back_populates="category",
        lazy="selectin",
    )
