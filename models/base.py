"""Base declarativa y mixins para modelos SQLAlchemy."""

from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos."""

    pass


# Tipos reutilizables
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(default=datetime.utcnow),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    ),
]


class TimestampMixin:
    """Mixin que agrega created_at y updated_at."""

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
