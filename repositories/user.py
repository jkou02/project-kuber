"""Repositorio de usuarios."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.base import Repository


class UserRepository(Repository[User]):
    """Repositorio para operaciones de usuario."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def find_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
