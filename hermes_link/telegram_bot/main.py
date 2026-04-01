"""Entry point for hermes-link Telegram bot.

Usage:
    python -m hermes_link.telegram_bot.main

Environment:
    HERMES_LINK_TELEGRAM_BOT_TOKEN  — Telegram bot token from @BotFather
"""

import asyncio
import logging
import os
import sys

from hermes_link.telegram_bot import bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger("hermes-link.bot")


def main() -> None:
    token = os.environ.get("HERMES_LINK_TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error(
            "HERMES_LINK_TELEGRAM_BOT_TOKEN is not set.\n"
            "Get a token from @BotFather and run:\n"
            "  export HERMES_LINK_TELEGRAM_BOT_TOKEN=..."
        )
        sys.exit(1)

    application = bot.build_app(token)

    logger.info("Starting hermes-link Telegram bot (polling)...")
    asyncio.run(application.run_polling(drop_pending_updates=True))


if __name__ == "__main__":
    main()
