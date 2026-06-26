"""Repositorio de transacciones."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.transaction import Transaction
from repositories.base import Repository


class TransactionRepository(Repository[Transaction]):
    """Repositorio para operaciones de transacción."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Transaction)

    async def list_by_user(self, user_id: int, limit: int = 20) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def list_by_user_and_month(
        self, user_id: int, year: int, month: int
    ) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .where(func.extract("year", Transaction.transaction_date) == year)
            .where(func.extract("month", Transaction.transaction_date) == month)
            .order_by(Transaction.transaction_date.desc())
        )
        return list(result.scalars().all())
