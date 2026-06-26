"""Modelo de presupuesto mensual."""

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin, int_pk


class MonthlyBudget(Base, TimestampMixin):
    __tablename__ = "monthly_budgets"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "category_id",
            "month",
            "year",
            name="uix_monthly_budget_user_category_month_year",
        ),
    )

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(default="VES", nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="monthly_budgets")
    category: Mapped["Category | None"] = relationship(
        back_populates="monthly_budgets",
    )
