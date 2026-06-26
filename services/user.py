"""Servicio de usuario."""

from sqlalchemy.ext.asyncio import AsyncSession

from models.category import Category, CategoryType
from models.payment_method import PaymentMethod, PaymentMethodType
from models.user import User
from repositories.user import UserRepository

DEFAULT_CATEGORIES: list[tuple[str, CategoryType]] = [
    ("Comida", CategoryType.EXPENSE),
    ("Transporte", CategoryType.EXPENSE),
    ("Salud", CategoryType.EXPENSE),
    ("Medicina", CategoryType.EXPENSE),
    ("Entretenimiento", CategoryType.EXPENSE),
    ("Casa", CategoryType.EXPENSE),
    ("Educación", CategoryType.EXPENSE),
    ("Ropa", CategoryType.EXPENSE),
    ("Salario", CategoryType.INCOME),
    ("Freelance", CategoryType.INCOME),
    ("Inversiones", CategoryType.INCOME),
]

DEFAULT_PAYMENT_METHODS: list[tuple[str, PaymentMethodType, str]] = [
    ("Efectivo", PaymentMethodType.CASH, "VES"),
    ("Transferencia", PaymentMethodType.BANK, "VES"),
    ("Zelle", PaymentMethodType.BANK, "USD"),
]


class UserService:
    """Servicio para gestión de usuarios."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UserRepository(session)

    async def get_or_create_by_telegram_id(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
    ) -> User:
        user = await self.repo.find_by_telegram_id(telegram_id)
        if user:
            return user

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
        )
        await self.repo.create(user)
        await self.session.flush()

        for name, cat_type in DEFAULT_CATEGORIES:
            self.session.add(
                Category(
                    user_id=user.id,
                    name=name,
                    type=cat_type,
                    is_default=True,
                )
            )

        for name, pm_type, currency in DEFAULT_PAYMENT_METHODS:
            self.session.add(
                PaymentMethod(
                    user_id=user.id,
                    name=name,
                    type=pm_type,
                    currency=currency,
                    is_default=True,
                )
            )

        await self.session.commit()
        return user
