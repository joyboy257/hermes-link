"""Skill installer — handles various install_command types."""

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from . import registry
from .format import fmt_success, fmt_error, fmt_info, fmt_warn


INSTALL_BASE = Path.home() / ".hermes" / "skills"
TEMP_DIR = Path(tempfile.gettempdir()) / "hermes-link"


def _run(cmd: list[str], cwd: str | Path = None) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError as e:
        return -1, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return -1, "", str(e)


def _sh(cmd: str, timeout: int = 120) -> tuple[int, str, str]:
    """Run a shell command string. Returns (code, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def install(name: str, force: bool = False, dry_run: bool = False) -> tuple[bool, str]:
    """Install a skill by name.

    Handles install_command types:
      - uv tool install git+https://...  → git-based tool
      - curl -sL https://... -o ...        → download binary
      - npm install -g ...                → npm global
      - other shell commands
    """
    index = registry.get_index()
    skill = None
    for s in index:
        if s.get("name") == name:
            skill = s
            break

    if skill is None:
        return False, f"Skill '{name}' not found in registry."

    is_inst, _ = registry.is_installed(name)
    if is_inst and not force:
        return False, (
            f"Skill '{name}' is already installed. "
            "Use --force to reinstall."
        )

    install_cmd = skill.get("install_command", "")
    skill_path = skill.get("skill_md_path", "")
    category = skill.get("category", "other")
    version = skill.get("version", "1.0.0")

    # Resolve install path: skill_md_path is like "productivity/notion/SKILL.md"
    # The skill dir is the parent of the SKILL.md
    if skill_path:
        skill_dir = Path(skill_path).parent  # "productivity/notion"
    else:
        skill_dir = Path(category) / name

    install_path = INSTALL_BASE / skill_dir

    if dry_run:
        lines = [
            f"[dry-run] Would install {name}",
            f"  Category:   {category}",
            f"  Version:    {version}",
            f"  Path:       {install_path}",
            f"  Install:    {install_cmd}",
        ]
        prereqs = skill.get("prerequisites", {})
        env_vars = prereqs.get("env_vars", []) if isinstance(prereqs, dict) else []
        if env_vars:
            lines.append(f"  Env vars:   {', '.join(env_vars)}")
        return True, "\n".join(lines)

    # Pre-clean on force (regardless of prior install status)
    if force and install_cmd:
        import re as _re
        clone_match = _re.search(r"clone\s+[^\s]+\s+(~/[^\s]+)", install_cmd)
        if clone_match:
            dest = Path(clone_match.group(1).replace("~", str(Path.home())))
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)

    # Clean up existing tracked install
    if is_inst and force:
        if install_path.exists():
            shutil.rmtree(install_path, ignore_errors=True)

    # Instruction-only install commands — don't execute, just git sparse-clone the SKILL.md
    no_exec = (
        not install_cmd
        or install_cmd.startswith("echo")
        or install_cmd.startswith("print")
        or install_cmd.startswith("Set ")
        or install_cmd.startswith("set ")
        or install_cmd.startswith("Add ")
        or install_cmd.startswith("Configure ")
        or "No install needed" in install_cmd
        or "no-install" in install_cmd.lower()
    )

    if no_exec and skill_path:
        # Instruction-only: git sparse-clone the SKILL.md
        source = skill.get("source_repo", "")
        if source:
            success, msg = _install_git_sparse(name, source, skill_path, install_path)
        else:
            success, msg = False, "No install_command and no source_repo."
        if not success:
            return False, msg
    elif install_cmd:
        # Real install command — execute it
        if "uv tool install git+" in install_cmd or "pip install git+" in install_cmd:
            success, msg = _install_git_tool(name, install_cmd, install_path)
        elif install_cmd.startswith("curl") or install_cmd.startswith("wget"):
            success, msg = _install_curl_script(name, install_cmd, install_path)
        elif "npm install -g" in install_cmd or "pip install" in install_cmd:
            success, msg = _install_tool(name, install_cmd, install_path)
        else:
            code, stdout, stderr = _sh(install_cmd)
            if code != 0:
                success, msg = False, f"Install command failed: {stderr or stdout}"
            else:
                success, msg = True, stdout.strip() or f"Ran: {install_cmd}"
        if not success:
            return False, msg

    # Save install record
    record = {
        "name": name,
        "version": version,
        "category": category,
        "path": str(install_path),
        "installed_at": "",  # filled by caller
        "install_command": install_cmd,
    }
    registry.save_installed(name, record)

    return True, f"Installed {name} (v{version}) → {install_path}"


def _install_git_tool(name: str, cmd: str, install_path: Path) -> tuple[bool, str]:
    """Run a uv/pip tool install from git. Handles existing destination paths."""
    # Extract destination from command: "git clone https://... ~/.agent-skills/hamelnb"
    # or "uv tool install ..."
    import re as _re
    dest_match = _re.search(r"(?:clone|install).*?([^\s\"']*~/[^\s\"']+)", cmd)
    if dest_match:
        dest = Path(dest_match.group(1).replace("~", str(Path.home())))
        if dest.exists():
            shutil.rmtree(dest, ignore_errors=True)

    code, stdout, stderr = _sh(cmd)
    if code != 0:
        return False, f"Install failed: {stderr or stdout}"
    return True, stdout.strip() or f"Installed {name}"


def _install_curl_script(name: str, cmd: str, install_path: Path) -> tuple[bool, str]:
    """Download a script via curl and place it."""
    # Extract URL and destination from curl command
    # e.g. curl -sL https://... -o ~/.local/bin/openhue
    url_match = re.search(r"https?://[^\s\"']+", cmd)
    out_match = re.search(r"-o\s+([^\s\"']+)", cmd)
    if not url_match:
        return False, f"Could not parse URL from: {cmd}"

    url = url_match.group(0)
    out_path = Path(out_match.group(1)) if out_match else Path("/tmp") / name

    install_path.parent.mkdir(parents=True, exist_ok=True)

    code, _, stderr = _sh(f"curl -sL {url} -o {out_path}")
    if code != 0:
        return False, f"Download failed: {stderr}"

    out_path.chmod(0o755)
    return True, f"Downloaded to {out_path}"


def _install_tool(name: str, cmd: str, install_path: Path) -> tuple[bool, str]:
    """Run npm/pip install command."""
    code, stdout, stderr = _sh(cmd)
    if code != 0:
        return False, f"Install failed: {stderr or stdout}"
    return True, stdout or f"Installed {name}"


def _install_git_sparse(name: str, source_repo: str, skill_path: str, install_path: Path) -> tuple[bool, str]:
    """Sparse clone a skill directory from a git repo."""
    # Normalize source_repo to a git URL
    if source_repo.startswith("github.com/"):
        repo_url = f"https://{source_repo}.git"
    elif source_repo.startswith("git@"):
        repo_url = source_repo
    else:
        repo_url = source_repo  # already a full URL

    tmp = TEMP_DIR / f"install-{name}"
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True, exist_ok=True)

    # Step 1: clone --filter=blob:none --no-checkout
    code, _, stderr = _run(
        ["git", "clone", "--depth=1", "--filter=blob:none", "--no-checkout", repo_url, str(tmp)]
    )
    if code != 0:
        return False, f"git clone failed: {stderr}"

    # Step 2: sparse-checkout the skill dir
    code, _, stderr = _run(
        ["git", "sparse-checkout", "set", skill_path],
        cwd=tmp,
    )
    if code != 0:
        return False, f"git sparse-checkout failed: {stderr}"

    # Step 3: checkout
    code, _, stderr = _run(["git", "checkout"], cwd=tmp)
    if code != 0:
        return False, f"git checkout failed: {stderr}"

    src = tmp / skill_path
    if not src.exists():
        return False, f"Path {skill_path} not found in repository."

    # Copy to install location
    install_path.parent.mkdir(parents=True, exist_ok=True)
    if install_path.exists():
        shutil.rmtree(install_path, ignore_errors=True)

    # The skill dir in the repo may be nested; copy the parent directory
    # so that SKILL.md ends up at install_path/SKILL.md
    try:
        shutil.copytree(src, install_path)
    except OSError:
        # If it's a file not dir, copy parent
        parent = src.parent
        shutil.copytree(parent, install_path)

    shutil.rmtree(tmp, ignore_errors=True)
    return True, f"Cloned from {repo_url}/{skill_path}"


def uninstall(name: str) -> tuple[bool, str]:
    """Uninstall a skill."""
    path = registry.get_installed_path(name)
    if path is None:
        # Still check if the name is recorded
        installed = registry.get_installed()
        if name in installed:
            # Orphaned install — just remove record
            registry.remove_installed(name)
            return True, f"Removed install record for '{name}' (files may remain)."
        return False, f"Skill '{name}' is not installed."

    try:
        shutil.rmtree(path)
    except OSError as e:
        return False, f"Could not remove {path}: {e}"

    registry.remove_installed(name)
    return True, f"Removed {name} from {path}"


def update(name: str | None = None) -> list[tuple[str, bool, str]]:
    """Update installed skills. If name is None, update all."""
    results = []
    installed = registry.list_installed()

    if name:
        installed = [r for r in installed if r.get("name") == name]
        if not installed:
            return [(name, False, "Not installed.")]

    for record in installed:
        n = record.get("name")
        # Re-run install with force
        success, msg = install(n, force=True)
        results.append((n, success, msg))

    return results
