"""Entrypoint del bot de Telegram."""

import asyncio
import logging
import signal

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.handlers.add import (
    AMOUNT,
    CATEGORY,
    CURRENCY,
    DESCRIPTION,
    add_handler,
    amount_handler,
    cancel_handler,
    category_handler,
    currency_handler,
    description_handler,
)
from bot.handlers.categories import categories_handler
from bot.handlers.quick import quick_handler
from bot.handlers.start import start_handler
from bot.handlers.summary import summary_handler
from core.config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no está configurado.")
        return

    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("quick", quick_handler))
    application.add_handler(CommandHandler("summary", summary_handler))
    application.add_handler(CommandHandler("categories", categories_handler))

    add_conv = ConversationHandler(
        entry_points=[CommandHandler("add", add_handler)],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_handler)],
            CURRENCY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, currency_handler)
            ],
            CATEGORY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, category_handler)
            ],
            DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, description_handler)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
    )
    application.add_handler(add_conv)

    async def stop() -> None:
        await application.stop()
        await application.shutdown()

    def signal_handler(sig: int, frame: object) -> None:
        logger.info("Recibida señal %s, deteniendo bot...", sig)
        asyncio.create_task(stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Iniciando bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
