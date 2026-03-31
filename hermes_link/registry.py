"""Registry client — fetches and caches skill index from GitHub."""

import json
import os
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

INDEX_URL = "https://raw.githubusercontent.com/joyboy257/hermes-link/main/hermes-link-index.json"
CACHE_DIR = Path.home() / ".hermes" / ".cache" / "hermes-link"
CACHE_FILE = CACHE_DIR / "index.json"
INSTALLED_FILE = CACHE_DIR / "installed.json"
SKILLS_DIR = Path.home() / ".hermes" / "skills"
CACHE_TTL = 300  # seconds


def _request(url: str, timeout: int = 15) -> dict | None:
    try:
        req = Request(url, headers={"User-Agent": "hermes-link/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, json.JSONDecodeError, TimeoutError, OSError):
        return None


def fetch_index(force_refresh: bool = False) -> list[dict]:
    """Fetch the skill index. Falls back to cache on network failure."""
    cached = None
    if not force_refresh and CACHE_FILE.exists():
        try:
            mtime = CACHE_FILE.stat().st_mtime
            if time.time() - mtime < CACHE_TTL:
                cached = json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    fresh = _request(INDEX_URL)
    if fresh is not None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(fresh, indent=2))
        return fresh.get("skills", [])

    if cached is not None:
        return cached.get("skills", [])

    return []


def get_index() -> list[dict]:
    return fetch_index()


def get_installed() -> dict[str, dict]:
    """Get installed skills map: skill_name -> record."""
    if not INSTALLED_FILE.exists():
        return {}
    try:
        return json.loads(INSTALLED_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_installed(name: str, record: dict) -> None:
    """Save an installed skill record."""
    installed = get_installed()
    installed[name] = record
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    INSTALLED_FILE.write_text(json.dumps(installed, indent=2))


def remove_installed(name: str) -> bool:
    """Remove an installed skill record. Returns True if it was removed."""
    installed = get_installed()
    if name in installed:
        del installed[name]
        INSTALLED_FILE.write_text(json.dumps(installed, indent=2))
        return True
    return False


def is_installed(name: str) -> tuple[bool, str | None]:
    """Check if a skill is installed. Returns (installed, version_or_None)."""
    installed = get_installed()
    if name not in installed:
        return False, None
    return True, installed[name].get("version")


def get_installed_path(name: str) -> Path | None:
    """Find where a skill's SKILL.md is installed."""
    installed = get_installed()
    if name not in installed:
        return None
    path = Path(installed[name].get("path", ""))
    if path.exists() and (path / "SKILL.md").exists():
        return path
    return None


def list_installed() -> list[dict]:
    """List all installed skill records."""
    return list(get_installed().values())
