"""Modelo de fuente de ingreso."""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin, int_pk


class IncomeSource(Base, TimestampMixin):
    __tablename__ = "income_sources"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="income_sources")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="income_source",
        lazy="selectin",
    )
