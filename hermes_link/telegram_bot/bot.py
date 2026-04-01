"""python-telegram-bot Application setup for hermes-link Telegram bot."""

import logging
import os

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from . import commands

logger = logging.getLogger(__name__)

BOT_TOKEN_ENVVAR = "HERMES_LINK_TELEGRAM_BOT_TOKEN"


def _get_token() -> str | None:
    return os.environ.get(BOT_TOKEN_ENVVAR)


async def _post_init(application: Application) -> None:
    """After initialization, register command menu with Telegram."""
    await application.bot.set_my_commands([
        BotCommand("market", "hermes-link skill marketplace"),
    ])
    logger.info("Telegram command menu registered: /market")


def build_app(token: str | None = None) -> Application:
    """Build and return a configured telegram.ext.Application.

    If token is None, reads from HERMES_LINK_TELEGRAM_BOT_TOKEN env var.
    """
    if token is None:
        token = _get_token()
    if not token:
        raise ValueError(
            f"Bot token not provided and {BOT_TOKEN_ENVVAR} is not set. "
            "Set it with: export HERMES_LINK_TELEGRAM_BOT_TOKEN=..."
        )

    builder = (
        Application.builder()
        .token(token)
        .post_init(_post_init)
    )
    app = builder.build()

    # Register /market command and its subcommands
    # The handler accepts "market" (without leading slash) and dispatches
    # to sub-handlers based on the first argument.
    app.add_handler(
        CommandHandler(
            "market",
            commands.cmd_dispatch,
            filters=~filters.COMMAND,
        )
    )

    # Also register /markethelp as a standalone alias
    app.add_handler(
        CommandHandler("markethelp", commands.cmd_help)
    )

    logger.info("hermes-link Telegram bot initialized")
    return app
