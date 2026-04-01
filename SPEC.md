# hermes-link — MVP Specification

**Version:** 1.0.0  
**Status:** In Progress  
**Last Updated:** 2026-03-31

---

## 1. Concept & Vision

hermes-link is a skill marketplace for Hermes Agent — one command to browse, install, and manage capabilities. The MVP ships a Python CLI (`hermes-link`) callable from any Hermes session that fetches a JSON registry from GitHub and installs skills via sparse git clone.

The tone is minimal and fast. No fluff. Skills are discovered, installed, and forgotten about — because they just work.

---

## 2. Design Language

**Aesthetic:** Terminal-native. Monochrome with selective color. Think `ripgrep` meets `npm`.

**Colors:**
- Success / installed: green `#22c55e`
- Error / failed: red `#ef4444`
- Info / headers: blue `#3b82f6`
- Muted / secondary: gray `#6b7280`
- Reset: no color

**No emoji in CLI output.** Unicode symbols for structure only: `◆` `✦` `✓` `✗` `→`

**Typography:** Monospace. Everything aligns in columns.

---

## 3. CLI Specification

### 3.1 Command Interface

```
hermes-link [--version] [--help]
hermes-link list [--category <cat>] [--format json|table]
hermes-link search <query>
hermes-link info <skill-id>
hermes-link install <skill-id> [--force] [--dry-run]
hermes-link uninstall <skill-id>
hermes-link installed [--format json|table]
hermes-link update [<skill-id>]   # update one or all
```

### 3.2 Registry Source

- **URL:** `https://raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/index.json`
- **Local cache:** `~/.hermes/.cache/hermes-link/index.json` (refreshed on each call)
- **Offline mode:** If cache exists and network fails, use cache

### 3.3 Installation Location

Skills install to: `~/.hermes/skills/<category>/<skill-id>/`

Example: `hermes-link install notion-basic` → `~/.hermes/skills/productivity/notion-basic/`

### 3.4 Behavior

**`list`**
- Fetch index.json, print skills as aligned table: `ID  NAME  CATEGORY  DESCRIPTION`
- Filter by `--category` if provided
- Show `installed ✓` badge for already-installed skills

**`search`**
- Fuzzy match on name, description, tags (case-insensitive)
- Rank by match quality
- Print matching skills as compact table

**`info`**
- Print full manifest for a skill: version, author, tags, description, pricing
- Show local install status: installed (version X) or not installed

**`install`**
- Resolve skill ID → manifest → archive URL
- Download skill files via git sparse-clone (no full repo clone)
- Create category subdirectory if needed
- Write installed manifest to `.hermes-link/installed/<skill-id>.json`
- Print success + next steps if any prerequisites

**`uninstall`**
- Remove skill directory
- Remove installed manifest
- Print confirmation

**`installed`**
- List all skills in `~/.hermes/skills/` matching expected structure
- Cross-reference with registry for version comparison

**`update`**
- Check installed skills against registry
- Offer to update if newer version available
- `--all` to update everything

### 3.5 Error Handling

| Scenario | Response |
|----------|----------|
| Network failure | `✗ Could not reach registry. Check your connection.` |
| Skill not found | `✗ Skill '<id>' not found in registry.` |
| Already installed | `ℹ Skill '<id>' is already installed. Use --force to reinstall.` |
| Prereqs missing | `⚠ Prerequisites not met: [LIST]. Set these before using the skill.` |
| Install failed | `✗ Install failed: <reason>` |

---

## 4. Technical Approach

### 4.1 Stack

- **Language:** Python 3.10+
- **CLI framework:** argparse (stdlib, no dependencies)
- **HTTP:** urllib.request (stdlib)
- **Version control:** git (must be installed)

### 4.2 Architecture

```
hermes-link/
├── hermes_link/
│   ├── __init__.py
│   ├── cli.py          # argparse, commands
│   ├── registry.py    # fetch/parse index.json
│   ├── installer.py   # git sparse-clone, file ops
│   ├── format.py       # table formatting
│   └── telegram_bot/   # Telegram bot — /market commands
│       ├── __init__.py
│       ├── bot.py     # python-telegram-bot Application setup
│       ├── commands.py # /market dispatch + handlers
│       ├── formatters.py # Telegram-friendly output
│       └── main.py    # entry point
├── hermes_link.egg-info/
├── pyproject.toml
├── SPEC.md
├── README.md
└── registry/
    └── skills/
        ├── index.json
        ├── hermes-link/
        │   ├── SKILL.md
        │   └── manifest.json
        └── [other skills...]
```

### 4.3 Key Implementation Notes

**Sparse clone (no full repo checkout):**
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/joyboy257/hermes-link.git /tmp/hl-sparse
git sparse-checkout set registry/skills/<skill-id> /tmp/hl-sparse
cp -r /tmp/hl-sparse/registry/skills/<skill-id> ~/.hermes/skills/<category>/
```

**Local cache strategy:**
- Store at `~/.hermes/.cache/hermes-link/index.json`
- Always refresh (no stale reads) — cache is for offline fallback only

**Install manifest:**
- Stored at `~/.hermes/.cache/hermes-link/installed/<skill-id>.json`
- Contains: `{id, version, installed_at, manifest}`

---

## 5. File Outputs

### 5.1 Registry Index (`index.json`)

Maintained at `registry/skills/index.json` in the repo. Contains skill metadata for all available skills.

### 5.2 Skill Archive

Each skill lives at `registry/skills/<skill-id>/` with:
- `SKILL.md` — skill definition (YAML frontmatter + markdown)
- `manifest.json` — machine-readable metadata
- Any supporting files (scripts, templates)

---

## 6. MVP Scope

**In scope:**
- Python CLI with all commands in §3
- Registry JSON with 10+ seed skills
- Working install/uninstall of skills
- GitHub Pages hosting of registry
- Telegram bot (`/market list|search|info|install|installed|uninstall|help`)

**Out of scope (defer to Phase 2+):**
- Web dashboard
- User accounts / auth
- Ratings / reviews
- Premium / paid skills
- API server
- Search analytics

---

## 7. Registry Structure

```
registry/skills/
├── index.json                      # Master skill list
├── hermes-link/                     # The hermes-link CLI skill
│   ├── SKILL.md
│   └── manifest.json
├── notion-basic/
│   ├── SKILL.md
│   └── manifest.json
├── github-workflow/
│   ├── SKILL.md
│   └── manifest.json
├── twitter-tools/
│   ├── SKILL.md
│   └── manifest.json
└── [additional skills...]
    ├── SKILL.md
    └── manifest.json
```

---

## 8. Quality Bar

- CLI installs without errors on a clean Linux box
- `hermes-link list` returns results in < 2s
- `hermes-link install X` installs a skill correctly
- `hermes-link uninstall X` removes it cleanly
- All error cases produce helpful messages
- No external dependencies beyond Python 3.10 + git
