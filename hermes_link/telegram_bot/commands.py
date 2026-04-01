"""Telegram command handlers for hermes-link bot.

Handlers mirror the hermes-link CLI commands:
  /market list       — browse all skills
  /market search <q> — fuzzy search
  /market info <name> — full skill details
  /market install <name> — install a skill
  /market installed  — list installed skills
  /market uninstall <name> — remove a skill
"""

import asyncio
import logging
import re
from typing import Awaitable, Callable

from telegram import Update
from telegram.ext import ContextTypes

# Import hermes_link components
from hermes_link import registry, installer
from . import formatters

logger = logging.getLogger(__name__)

# Safe wrapper: run blocking code in executor to avoid blocking the event loop
def _run_sync(fn: Callable[[], object]) -> Awaitable[object]:
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, fn)


# ── helpers ──────────────────────────────────────────────────────────────────

async def _reply(update: Update, text: str, **kwargs) -> None:
    await update.message.reply_text(text, **kwargs)


def _parse_args(text: str, min_args: int = 0) -> tuple[bool, list[str]]:
    """Split command text into tokens, handling quoted args."""
    # text is like "/market install notion" or "/market info foo bar baz"
    tokens = re.findall(r'(?:[^\s"]+|"[^"]*")+', text)
    return len(tokens) >= min_args, tokens[1:]  # strip command name


# ── /market list ─────────────────────────────────────────────────────────────

async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all available skills from the registry."""
    await update.message.reply_text("Fetching marketplace...")

    def _do():
        skills = registry.get_index()
        installed = {rec.get("name") for rec in registry.list_installed()}
        return formatters.fmt_skills_list(skills, installed)

    text = await _run_sync(_do)
    await _reply(update, text)


# ── /market search ───────────────────────────────────────────────────────────

async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search skills by name, description, or tags."""
    if not context.args:
        await _reply(update, "Usage: /market search <query>\nExample: /market search github")
        return

    query = " ".join(context.args).lower()

    def _do():
        skills = registry.get_index()
        installed = {rec.get("name") for rec in registry.list_installed()}

        if not query:
            return formatters.fmt_skills_list(skills, installed)

        # Fuzzy match: name, description, tags
        matched = []
        for s in skills:
            name = s.get("name", "").lower()
            desc = s.get("description", "").lower()
            tags = " ".join(s.get("tags", [])).lower()
            if query in name or query in desc or query in tags:
                matched.append(s)

        # Sort: exact name match first
        matched.sort(key=lambda s: 0 if s.get("name", "").lower() == query else 1)
        return formatters.fmt_search_results(matched, query, installed)

    text = await _run_sync(_do)
    await _reply(update, text)


# ── /market info ─────────────────────────────────────────────────────────────

async def cmd_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show full details for a specific skill."""
    if not context.args:
        await _reply(update, "Usage: /market info <skill-name>\nExample: /market info notion")
        return

    name = " ".join(context.args)

    def _do():
        skills = registry.get_index()
        skill = None
        for s in skills:
            if s.get("name") == name:
                skill = s
                break

        if skill is None:
            return formatters.fmt_skill_not_found(name)

        is_inst, ver = registry.is_installed(name)
        return formatters.fmt_skill_info(skill, is_inst, ver)

    text = await _run_sync(_do)
    await _reply(update, text)


# ── /market install ───────────────────────────────────────────────────────────

async def cmd_install(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Install a skill by name."""
    if not context.args:
        await _reply(update, "Usage: /market install <skill-name>\nExample: /market install notion")
        return

    name = " ".join(context.args)
    await update.message.reply_text(f"Installing {name}...")

    def _do():
        success, msg = installer.install(name, force=False)
        if success:
            return formatters.fmt_install_success(name)
        return formatters.fmt_install_error(name, msg)

    text = await _run_sync(_do)
    await _reply(update, text)


# ── /market installed ────────────────────────────────────────────────────────

async def cmd_installed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all installed skills."""
    def _do():
        skills = registry.list_installed()
        return formatters.fmt_installed(skills)

    text = await _run_sync(_do)
    await _reply(update, text)


# ── /market uninstall ────────────────────────────────────────────────────────

async def cmd_uninstall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove an installed skill."""
    if not context.args:
        await _reply(update, "Usage: /market uninstall <skill-name>\nExample: /market uninstall notion")
        return

    name = " ".join(context.args)

    def _do():
        success, msg = installer.uninstall(name)
        if success:
            return formatters.fmt_uninstall_success(name)
        return formatters.fmt_uninstall_error(name, msg)

    text = await _run_sync(_do)
    await _reply(update, text)


# ── /market help ─────────────────────────────────────────────────────────────

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help for all /market commands."""
    lines = [
        "◆ hermes-link bot — skill marketplace",
        "",
        "/market list        — Browse all available skills",
        "/market search <q>  — Search by name or keyword",
        "/market info <name> — Skill details and install command",
        "/market install <n> — Install a skill",
        "/market installed   — List your installed skills",
        "/market uninstall <n> — Remove a skill",
        "/market help        — Show this message",
        "",
        "Skills install to ~/.hermes/skills/",
    ]
    await _reply(update, "\n".join(lines))


# ── dispatcher ───────────────────────────────────────────────────────────────

async def cmd_dispatch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route /market <subcommand> to the appropriate handler."""
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    # text is like "/market list" or "/market install foo"
    tokens = re.findall(r'(?:[^\s"]+|"[^"]*")+', text)
    if len(tokens) < 2:
        # No subcommand — show help
        await cmd_help(update, context)
        return

    subcommand = tokens[1].lower()
    args = tokens[2:] if len(tokens) > 2 else []

    # Map subcommand name to handler + whether it expects args
    DISPATCH: dict[str, tuple] = {
        "list":      (cmd_list, False),
        "search":    (cmd_search, False),
        "info":      (cmd_info, False),
        "install":   (cmd_install, False),
        "installed": (cmd_installed, False),
        "uninstall": (cmd_uninstall, False),
        "help":      (cmd_help, False),
    }

    if subcommand not in DISPATCH:
        await _reply(
            update,
            f"Unknown command {subcommand!r}. Run /market help for usage.",
        )
        return

    handler, _ = DISPATCH[subcommand]
    # Build a mock namespace for handlers that expect args via context.args
    context.args = args
    await handler(update, context)
