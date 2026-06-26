"""Modelo de tasa de cambio."""

from datetime import date

from sqlalchemy import Date, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin, int_pk


class ExchangeRate(Base, TimestampMixin):
    __tablename__ = "exchange_rates"
    __table_args__ = (
        UniqueConstraint(
            "from_currency",
            "to_currency",
            "date",
            name="uix_exchange_rate_pair_date",
        ),
    )

    id: Mapped[int_pk]
    from_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    to_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    rate: Mapped[float] = mapped_column(Numeric(20, 10), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
