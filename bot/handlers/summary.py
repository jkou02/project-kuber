"""Handler para el comando /summary."""

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from core.database import AsyncSessionLocal
from services.transaction import TransactionService
from services.user import UserService


async def summary_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra resumen del mes actual."""
    tg_user = update.effective_user
    if not tg_user:
        return

    now = datetime.now()
    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user = await user_service.get_or_create_by_telegram_id(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
        )
        tx_service = TransactionService(session)
        summary = await tx_service.get_monthly_summary(user.id, now.year, now.month)

    await update.message.reply_text(
        f"Resumen de {now.month:02d}/{now.year}\n"
        f"Ingresos: {summary['income']}\n"
        f"Gastos: {summary['expense']}\n"
        f"Flujo neto: {summary['net']}\n"
        f"Movimientos: {summary['count']}"
    )
