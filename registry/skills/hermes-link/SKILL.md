---
name: hermes-link
description: Browse, install, and manage Hermes Agent skills from the hermes-link marketplace. One command to discover, install, and manage capabilities.
version: 1.0.0
author: hermes-link
license: MIT
prerequisites:
  env_vars: []
metadata:
  hermes:
    homepage: https://github.com/joyboy257/hermes-link
    tags: [marketplace, skills, discovery, install, hermes-link]
---

# hermes-link

Skill marketplace CLI for Hermes Agent. Browse and install capabilities with one command.

## Installation

```bash
pip install hermes-link
# or
uv tool install git+https://github.com/joyboy257/hermes-link.git
```

Or use the CLI directly:

```bash
python3 -m hermes_link.cli --help
```

## Commands

```
hermes-link list                    # Browse all skills
hermes-link list --category mlops   # Filter by category
hermes-link search <query>          # Search by name/tag/description
hermes-link info <name>             # Full skill details
hermes-link install <name>          # Install a skill
hermes-link install <name> --force   # Reinstall
hermes-link uninstall <name>         # Remove a skill
hermes-link installed                # List installed skills
hermes-link installed -v             # Show install paths
hermes-link update                   # Update all installed skills
hermes-link update <name>            # Update one skill
```

## Quick Start

```bash
# See what's available
hermes-link list

# Install a skill
hermes-link install notion

# Search
hermes-link search github
```

## Categories

productivity | mlops | research | github | social-media | data-science | creative | gaming | smart-home | email | note-taking | leisure

## Registry

Skills are published at: github.com/joyboy257/hermes-link

Index: hermes-link-index.json (17 skills and growing)

## How It Works

hermes-link reads the registry index (hermes-link-index.json) which maps each skill to:
- A `skill_md_path` — where the SKILL.md lives in the repo
- An `install_command` — how to install the capability (uv, curl, npm, etc.)
- Metadata — name, description, category, tags, author

When you `install`, hermes-link either:
1. Runs the `install_command` (for tool-based skills like uv/npm packages)
2. Git sparse-clones the `skill_md_path` from the source repo

## Troubleshooting

**Network errors:** hermes-link fetches the registry from GitHub. If network is unavailable, it falls back to cached data.

**Install fails:** Check that the install_command is still valid and external dependencies are available.

**Skill not found:** The skill may have been removed or renamed. Run `hermes-link list` to see current offerings.
