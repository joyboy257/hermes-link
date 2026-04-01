"""Telegram output formatters for hermes-link bot."""

# Unicode symbols — no emoji, per hermes-link design language
BULLET = "◆"
CHECK = "OK"
CROSS = "FAIL"
INFO = "i"
WARN = "!"
BOLD_MARKER = "*"
CODE_MARKER = "`"


def _bold(text: str) -> str:
    return f"{BOLD_MARKER}{text}{BOLD_MARKER}"


def _code(text: str) -> str:
    return f"{CODE_MARKER}{text}{CODE_MARKER}"


# ── skill list ──────────────────────────────────────────────────────────────

def fmt_skills_list(skills: list[dict], installed_names: set[str]) -> str:
    """Format skill catalog as a compact Telegram message."""
    if not skills:
        return f"{CROSS} No skills found in registry."

    lines = [f"{BOLD_MARKER}hermes-link marketplace{BOLD_MARKER}  ({len(skills)} skills)\n"]

    # Group by category
    by_cat: dict[str, list[dict]] = {}
    for s in skills:
        cat = s.get("category", "misc") or "misc"
        by_cat.setdefault(cat, []).append(s)

    for cat, cat_skills in by_cat.items():
        lines.append(f"\n{BULLET} {cat.upper()}")
        for s in cat_skills:
            name = s.get("name", "?")
            desc = s.get("description", "")[:55]
            inst = f"  [{CHECK}]" if name in installed_names else ""
            lines.append(f"  {name}{inst}  {desc}")

    lines.append(f"\nUse /market info <name> for details, /market install <name> to install.")
    return "\n".join(lines)


def fmt_search_results(skills: list[dict], query: str, installed_names: set[str]) -> str:
    """Format search results."""
    if not skills:
        return f"{CROSS} No skills matching {query!r}."

    lines = [f"{BOLD_MARKER}Search: {query!r}{BOLD_MARKER}  ({len(skills)} result(s))\n"]
    for s in skills:
        name = s.get("name", "?")
        cat = s.get("category", "")
        inst = f"  [{CHECK}]" if name in installed_names else ""
        desc = s.get("description", "")[:60]
        lines.append(f"{BULLET} {name} [{cat}]{inst}\n  {desc}")
    return "\n".join(lines)


# ── skill info ──────────────────────────────────────────────────────────────

def fmt_skill_info(skill: dict, installed: bool, version: str | None = None) -> str:
    """Format full skill info."""
    name = skill.get("name", "?")
    desc = skill.get("description", "")
    cat = skill.get("category", "")
    author = skill.get("author", "")
    tags = skill.get("tags", [])
    prereqs = skill.get("prerequisites", {}) or {}

    lines = [
        f"{BULLET} {BOLD_MARKER}{name}{BOLD_MARKER}  (v{skill.get('version', '?')})",
        f"  Category: {cat}",
        f"  Author: {author}",
        f"\n{desc}",
    ]

    if tags:
        lines.append(f"\nTags: {', '.join(tags)}")

    if installed:
        ver_str = f"v{version}" if version else ""
        lines.append(f"\n{CHECK} Installed {ver_str}")
    else:
        lines.append(f"\n{CROSS} Not installed")
        prereq_list = prereqs.get("env_vars", []) if isinstance(prereqs, dict) else []
        if prereq_list:
            lines.append(f"\n{WARN} Prerequisites:")
            for var in prereq_list:
                lines.append(f"  - Set {var} in your environment")

    install_cmd = skill.get("install_command", "")
    if install_cmd:
        lines.append(f"\nInstall: {install_cmd[:80]}")

    return "\n".join(lines)


# ── installed list ──────────────────────────────────────────────────────────

def fmt_installed(skills: list[dict]) -> str:
    """Format installed skills list."""
    if not skills:
        return f"{INFO} No skills installed yet. Browse /market list to find some."

    lines = [f"{BOLD_MARKER}Installed skills{BOLD_MARKER}  ({len(skills)})\n"]
    for s in skills:
        name = s.get("name", "?")
        cat = s.get("category", "")
        ver = s.get("version", "")
        lines.append(f"{CHECK} {name}  [{cat}]  v{ver}")
    return "\n".join(lines)


# ── operation results ───────────────────────────────────────────────────────

def fmt_install_success(name: str) -> str:
    return f"{CHECK} Installed {name}. Use /market info {name} to learn more."


def fmt_install_error(name: str, reason: str) -> str:
    return f"{CROSS} Install failed for {name}: {reason}"


def fmt_uninstall_success(name: str) -> str:
    return f"{CHECK} Removed {name}."


def fmt_uninstall_error(name: str, reason: str) -> str:
    return f"{CROSS} Uninstall failed for {name}: {reason}"


def fmt_skill_not_found(name: str) -> str:
    return f"{CROSS} Skill {name!r} not found. Run /market list to see all skills."
