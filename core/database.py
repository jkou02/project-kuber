"""Configuración de sesiones y conexión a base de datos."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Convertir URL sync a async para SQLAlchemy 2.0
# postgresql:// -> postgresql+asyncpg://
DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

engine = create_async_engine(DATABASE_URL, echo=settings.is_development)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Dependency para obtener sesión de base de datos en FastAPI."""
    async with AsyncSessionLocal() as session:
        yield session
