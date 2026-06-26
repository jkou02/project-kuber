"""Repositorio de categorías."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.category import Category
from repositories.base import Repository


class CategoryRepository(Repository[Category]):
    """Repositorio para operaciones de categoría."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)

    async def find_by_name(self, user_id: int, name: str) -> Category | None:
        result = await self.session.execute(
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.name.ilike(name))
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> list[Category]:
        result = await self.session.execute(
            select(Category)
            .where(Category.user_id == user_id)
            .order_by(Category.name)
        )
        return list(result.scalars().all())

    async def get_defaults(self) -> list[Category]:
        result = await self.session.execute(
            select(Category).where(Category.is_default.is_(True))
        )
        return list(result.scalars().all())
