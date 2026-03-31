"""Output formatting for hermes-link CLI."""

# ANSI color codes (stripped if not a TTY)
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _c(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


def _pad(text: str, width: int) -> str:
    return text[:width].ljust(width)


def fmt_header(label: str) -> str:
    """Section header."""
    return f"\n  {BOLD}{label}{RESET}\n"


def fmt_table(skills: list[dict], installed: set[str] = None, max_width: int = 120) -> str:
    """Format skills as an aligned table."""
    if installed is None:
        installed = set()
    if not skills:
        return f"  {GRAY}No skills found.{RESET}"

    id_w = min(30, max(len(s.get("name", "")) for s in skills) + 2)
    cat_w = min(16, max(len(s.get("category", "") or "") for s in skills) + 2)
    avail = max_width - id_w - cat_w - 8
    desc_w = max(avail, 30)

    rows = []
    rows.append(f"  {_pad('NAME', id_w)} {_pad('CATEGORY', cat_w)} DESCRIPTION")
    rows.append(f"  {'-'*id_w} {'-'*cat_w} {'-'*desc_w}")

    for s in skills:
        name = s.get("name", "")
        cat = s.get("category", "") or ""
        desc = s.get("description", "")[:desc_w].ljust(desc_w)
        inst = _c(" installed", GREEN) if name in installed else ""
        rows.append(f"  {_pad(name, id_w)} {_pad(cat, cat_w)} {desc}{inst}")

    return "\n".join(rows)


def fmt_table_compact(skills: list[dict], installed: set[str] = None) -> str:
    """Compact format for search results."""
    if installed is None:
        installed = set()
    if not skills:
        return f"  {GRAY}No matches.{RESET}"

    lines = []
    for s in skills:
        name = s.get("name", "")
        cat = s.get("category", "")
        inst = _c(" ✓", GREEN) if name in installed else ""
        desc = s.get("description", "")[:60]
        lines.append(f"  {name}  [{cat}]{inst}")
        lines.append(f"    {desc}")
    return "\n".join(lines)


def fmt_info(skill: dict, is_installed: bool, version: str | None = None,
             install_path=None) -> str:
    """Format full skill info."""
    lines = [f"\n{'='*60}"]
    lines.append(f"  {BOLD}{_c(skill.get('name', ''), BLUE)}{RESET}  (v{skill.get('version', '?')})")

    if is_installed:
        ver_str = f"v{version}" if version else ""
        lines.append(f"  {_c('✓ Installed', GREEN)} {ver_str}")
        if install_path:
            lines.append(f"    {install_path}")
    else:
        lines.append(f"  {GRAY}Not installed{RESET}")

    lines.append(f"{'='*60}")
    lines.append(f"  Name:      {skill.get('name', '')}")
    lines.append(f"  Category:  {skill.get('category', '')}")
    lines.append(f"  Author:    {skill.get('author', '')}")
    tags = skill.get("tags", [])
    if tags:
        lines.append(f"  Tags:      {', '.join(tags)}")

    install_cmd = skill.get("install_command", "")
    if install_cmd:
        lines.append(f"  Install:   {install_cmd[:70]}")

    desc = skill.get("description", "")
    if desc:
        lines.append(f"\n  {desc}")

    prereqs = skill.get("prerequisites", {}) or {}
    env_vars = prereqs.get("env_vars", []) if isinstance(prereqs, dict) else []
    if env_vars:
        lines.append(f"\n  {_c('⚠ Prerequisites:', YELLOW)}")
        for var in env_vars:
            lines.append(f"    - Set {BOLD}{var}{RESET} in your environment")

    return "\n".join(lines)


def fmt_success(msg: str) -> str:
    return f"  {_c('✓', GREEN)} {msg}"


def fmt_error(msg: str) -> str:
    return f"  {_c('✗', RED)} {msg}"


def fmt_info2(msg: str) -> str:
    return f"  {_c('ℹ', BLUE)} {msg}"


def fmt_warn(msg: str) -> str:
    return f"  {_c('⚠', YELLOW)} {msg}"
