"""Handler para el comando /quick."""

from decimal import Decimal, InvalidOperation

from telegram import Update
from telegram.ext import ContextTypes

from core.database import AsyncSessionLocal
from services.transaction import TransactionService
from services.user import UserService


async def quick_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Registra una transacción en lenguaje natural.

    Formato esperado: /quick <tipo> <monto> <moneda> <categoría> [descripción]
    Ejemplo: /quick gasto 5 USD comida almuerzo
    """
    tg_user = update.effective_user
    if not tg_user:
        return

    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text(
            "Uso: /quick <tipo> <monto> <moneda> <categoría> [descripción]\n"
            "Ejemplo: /quick gasto 5 USD comida almuerzo"
        )
        return

    parts = text.split()
    if len(parts) < 4:
        await update.message.reply_text(
            "Faltan datos. Ejemplo: /quick gasto 5 USD comida almuerzo"
        )
        return

    type_str = parts[0].lower()
    if type_str in ("gasto", "g", "expense", "e"):
        tx_type = "expense"
    elif type_str in ("ingreso", "i", "income", "in"):
        tx_type = "income"
    else:
        await update.message.reply_text("Tipo debe ser 'gasto' o 'ingreso'.")
        return

    try:
        amount = Decimal(parts[1])
    except InvalidOperation:
        await update.message.reply_text("Monto inválido.")
        return

    currency = parts[2].upper()
    category_name = parts[3]
    description = " ".join(parts[4:]) if len(parts) > 4 else None

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user = await user_service.get_or_create_by_telegram_id(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
        )
        tx_service = TransactionService(session)
        try:
            tx = await tx_service.create_transaction(
                user_id=user.id,
                type_str=tx_type,
                amount=amount,
                currency=currency,
                category_name=category_name,
                description=description,
            )
            label = "Gasto" if tx_type == "expense" else "Ingreso"
            await update.message.reply_text(
                f"{label} registrado: {tx.amount} {tx.currency} en {tx.category.name}"
            )
        except Exception as exc:
            await update.message.reply_text(f"Error: {exc}")
