"""Servicio de transacciones."""

from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from models.category import Category
from models.payment_method import PaymentMethod
from models.transaction import Transaction, TransactionType
from repositories.category import CategoryRepository
from repositories.transaction import TransactionRepository


class TransactionService:
    """Servicio para creación y consulta de transacciones."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TransactionRepository(session)
        self.category_repo = CategoryRepository(session)

    async def create_transaction(
        self,
        user_id: int,
        type_str: str,
        amount: Decimal,
        currency: str,
        category_name: str,
        description: str | None = None,
        payment_method_id: int | None = None,
    ) -> Transaction:
        category = await self.category_repo.find_by_name(user_id, category_name)
        if not category:
            defaults = await self.category_repo.get_defaults()
            category = next(
                (c for c in defaults if c.name.lower() == category_name.lower()),
                None,
            )
        if not category:
            raise NotFoundError(f"Categoría '{category_name}' no encontrada.")

        if payment_method_id is None:
            result = await self.session.execute(
                select(PaymentMethod)
                .where(PaymentMethod.user_id == user_id)
                .limit(1)
            )
            pm = result.scalar_one_or_none()
            if not pm:
                raise NotFoundError("No hay métodos de pago configurados.")
            payment_method_id = pm.id

        transaction = Transaction(
            user_id=user_id,
            category_id=category.id,
            payment_method_id=payment_method_id,
            type=TransactionType(type_str),
            amount=amount,
            currency=currency,
            description=description,
            transaction_date=date.today(),
        )
        await self.repo.create(transaction)
        await self.session.commit()
        return transaction

    async def get_monthly_summary(
        self, user_id: int, year: int, month: int
    ) -> dict[str, object]:
        transactions = await self.repo.list_by_user_and_month(user_id, year, month)
        income = Decimal("0")
        expense = Decimal("0")
        for tx in transactions:
            if tx.type == TransactionType.INCOME:
                income += Decimal(str(tx.amount))
            else:
                expense += Decimal(str(tx.amount))
        return {
            "income": income,
            "expense": expense,
            "net": income - expense,
            "count": len(transactions),
        }
