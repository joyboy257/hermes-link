"""hermes-link CLI — skill marketplace client."""

import argparse
import sys
import time

from . import __version__
from . import registry
from . import installer
from .format import (
    fmt_table,
    fmt_table_compact,
    fmt_info,
    fmt_success,
    fmt_error,
    fmt_info2,
    fmt_warn,
    fmt_header,
)


def _installed_names() -> set[str]:
    return {rec.get("name") for rec in registry.list_installed()}


# ── commands ────────────────────────────────────────────────────────────────

def cmd_list(args) -> int:
    skills = registry.get_index()
    if not skills:
        print(fmt_error("Could not fetch skill index. Check your network."))
        return 1

    if args.category:
        skills = [s for s in skills if s.get("category") == args.category]

    if not skills:
        print(fmt_error(f"No skills in category '{args.category}'."))
        return 0

    installed = _installed_names()
    print(fmt_header(f"hermes-link marketplace — {len(skills)} skill(s)"))
    print(fmt_table(skills, installed, max_width=args.width))
    return 0


def cmd_search(args) -> int:
    skills = registry.get_index()
    if not skills:
        print(fmt_error("Could not fetch skill index. Check your network."))
        return 1

    q = args.query.lower()
    scored = []
    for s in skills:
        hay = " ".join([
            s.get("name", ""),
            s.get("description", ""),
            " ".join(s.get("tags", [])),
            s.get("category", ""),
        ]).lower()
        if q in hay:
            score = 0
            if q in s.get("name", "").lower():
                score += 10
            if q in s.get("category", "").lower():
                score += 3
            scored.append((score, s))

    scored.sort(key=lambda x: -x[0])
    results = [s for _, s in scored]

    installed = _installed_names()
    header = f"Search: '{args.query}' — {len(results)} result(s)"
    print(fmt_header(header))
    print(fmt_table_compact(results, installed))
    return 0


def cmd_info(args) -> int:
    skills = registry.get_index()
    skill = None
    for s in skills:
        if s.get("name") == args.name:
            skill = s
            break

    if skill is None:
        print(fmt_error(f"Skill '{args.name}' not found in registry."))
        return 1

    is_inst, ver = registry.is_installed(args.name)
    installed_path = registry.get_installed_path(args.name) if is_inst else None
    print(fmt_info(skill, is_inst, ver, installed_path))
    return 0


def cmd_install(args) -> int:
    success, msg = installer.install(
        args.name,
        force=args.force,
        dry_run=args.dry_run,
    )
    if success:
        print(fmt_success(msg))
        # Print prerequisites if any
        index = registry.get_index()
        skill = next((s for s in index if s.get("name") == args.name), None)
        if skill:
            prereqs = skill.get("prerequisites", {}) or {}
            env_vars = prereqs.get("env_vars", []) if isinstance(prereqs, dict) else []
            if env_vars:
                print(f"\n{fmt_warn('Prerequisites:')}")
                for var in env_vars:
                    print(f"  Set {var} in your environment before using this skill.")
        return 0
    else:
        print(fmt_error(msg))
        return 1


def cmd_uninstall(args) -> int:
    success, msg = installer.uninstall(args.name)
    if success:
        print(fmt_success(msg))
        return 0
    else:
        print(fmt_error(msg))
        return 1


def cmd_installed(args) -> int:
    installed = registry.list_installed()
    if not installed:
        print(fmt_info2("No skills installed. Run 'hermes-link list' to browse."))
        return 0

    print(fmt_header(f"Installed skills — {len(installed)}"))

    # Cross-reference with registry for latest versions
    skills_index = {s.get("name"): s for s in registry.get_index()}

    for rec in installed:
        name = rec.get("name", "?")
        ver = rec.get("version", "?")
        path = rec.get("path", "?")
        latest = skills_index.get(name, {}).get("version", ver)
        if latest != ver:
            status = fmt_warn(f"v{latest} available")
        else:
            status = fmt_success("up to date")
        print(f"  {name}  v{ver}  [{ver}]  {status}")
        if args.verbose:
            print(f"    {path}")
    return 0


def cmd_update(args) -> int:
    if args.name:
        results = installer.update(args.name)
    else:
        results = installer.update()

    if not results:
        print(fmt_info2("No installed skills to update."))
        return 0

    ok = fail = 0
    for name, success, msg in results:
        if success:
            print(fmt_success(f"{name}: {msg}"))
            ok += 1
        else:
            print(fmt_error(f"{name}: {msg}"))
            fail += 1
    return 0 if fail == 0 else 1


# ── main ────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="hermes-link",
        description="Skill marketplace for Hermes Agent.",
    )
    parser.add_argument("--version", action="version", version=f"hermes-link {__version__}")
    parser.add_argument(
        "--width", type=int, default=120,
        help="Terminal width for table formatting"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p = sub.add_parser("list", help="List available skills")
    p.add_argument("--category", help="Filter by category")
    p.set_defaults(func=cmd_list)

    # search
    p = sub.add_parser("search", help="Search skills")
    p.add_argument("query", help="Search query")
    p.set_defaults(func=cmd_search)

    # info
    p = sub.add_parser("info", help="Show skill details")
    p.add_argument("name", help="Skill name")
    p.set_defaults(func=cmd_info)

    # install
    p = sub.add_parser("install", help="Install a skill")
    p.add_argument("name", help="Skill name to install")
    p.add_argument("--force", action="store_true", help="Reinstall if already installed")
    p.add_argument("--dry-run", action="store_true", help="Show what would be installed")
    p.set_defaults(func=cmd_install)

    # uninstall
    p = sub.add_parser("uninstall", help="Uninstall a skill")
    p.add_argument("name", help="Skill name to remove")
    p.set_defaults(func=cmd_uninstall)

    # installed
    p = sub.add_parser("installed", help="List installed skills")
    p.add_argument("-v", "--verbose", action="store_true", help="Show install paths")
    p.set_defaults(func=cmd_installed)

    # update
    p = sub.add_parser("update", help="Update installed skills")
    p.add_argument("name", nargs="?", help="Skill name (omit to update all)")
    p.set_defaults(func=cmd_update)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
