"""Handler para el comando /start."""

from telegram import Update
from telegram.ext import ContextTypes

from core.database import AsyncSessionLocal
from services.user import UserService


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja /start creando el usuario si no existe."""
    tg_user = update.effective_user
    if not tg_user:
        return

    async with AsyncSessionLocal() as session:
        service = UserService(session)
        user = await service.get_or_create_by_telegram_id(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
        )

    name = user.first_name or user.username or "usuario"
    await update.message.reply_text(f"¡Bienvenido a KuberCalc, {name}!")
