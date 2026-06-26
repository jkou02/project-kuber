"""Handler para el comando /categories."""

from telegram import Update
from telegram.ext import ContextTypes

from core.database import AsyncSessionLocal
from repositories.category import CategoryRepository
from services.user import UserService


async def categories_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista las categorías del usuario."""
    tg_user = update.effective_user
    if not tg_user:
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user = await user_service.get_or_create_by_telegram_id(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
        )

        cat_repo = CategoryRepository(session)
        categories = await cat_repo.get_by_user(user_id=user.id)

        if not categories:
            await update.message.reply_text("No tienes categorías configuradas.")
            return

        lines = ["📂 *Tus categorías:*\n"]
        for cat in categories:
            icon = "💸" if cat.type.value == "expense" else "💰"
            lines.append(f"{icon} {cat.name}")

        await update.message.reply_text(
            "\n".join(lines),
            parse_mode="Markdown",
        )
