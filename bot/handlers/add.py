"""Handler para el comando /add con flujo conversacional."""

from decimal import Decimal, InvalidOperation

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from core.database import AsyncSessionLocal
from services.transaction import TransactionService
from services.user import UserService

AMOUNT, CURRENCY, CATEGORY, DESCRIPTION = range(4)


async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia el flujo de registro paso a paso."""
    tg_user = update.effective_user
    if not tg_user:
        return ConversationHandler.END

    context.user_data["tg_user_id"] = tg_user.id
    context.user_data["tg_username"] = tg_user.username
    context.user_data["tg_first_name"] = tg_user.first_name

    await update.message.reply_text("¿Cuál es el monto?")
    return AMOUNT


async def amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    try:
        context.user_data["amount"] = Decimal(text)
    except InvalidOperation:
        await update.message.reply_text("Monto inválido. Intenta de nuevo:")
        return AMOUNT

    await update.message.reply_text("¿Qué moneda? (ej. VES, USD)")
    return CURRENCY


async def currency_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["currency"] = update.message.text.strip().upper()
    await update.message.reply_text("¿Qué categoría? (ej. comida, transporte)")
    return CATEGORY


async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["category"] = update.message.text.strip()
    await update.message.reply_text("¿Descripción? (o escribe 'no' para omitir)")
    return DESCRIPTION


async def description_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["description"] = None if text.lower() == "no" else text

    category = context.user_data["category"].lower()
    if category in ("salario", "sueldo", "ingreso", "freelance"):
        tx_type = "income"
    else:
        tx_type = "expense"

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user = await user_service.get_or_create_by_telegram_id(
            telegram_id=context.user_data["tg_user_id"],
            username=context.user_data.get("tg_username"),
            first_name=context.user_data.get("tg_first_name"),
        )
        tx_service = TransactionService(session)
        try:
            tx = await tx_service.create_transaction(
                user_id=user.id,
                type_str=tx_type,
                amount=context.user_data["amount"],
                currency=context.user_data["currency"],
                category_name=context.user_data["category"],
                description=context.user_data["description"],
            )
            await update.message.reply_text(
                f"Transacción registrada: {tx.amount} {tx.currency} ({tx.category.name})"
            )
        except Exception as exc:
            await update.message.reply_text(f"Error al guardar: {exc}")

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operación cancelada.")
    context.user_data.clear()
    return ConversationHandler.END
