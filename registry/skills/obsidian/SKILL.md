---
name: obsidian
description: Manage your Obsidian vault from the terminal. Search notes, create entries, link knowledge, and query your second brain.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: [OBSIDIAN_VAULT_PATH]
metadata:
  hermes:
    tags: [obsidian, notes, knowledge-base, markdown]
---

# obsidian

Access your Obsidian vault without opening the app.

## Setup

1. Set your vault path:
```bash
export OBSIDIAN_VAULT_PATH="$HOME/notes/vault"
```

2. Enable the Obsidian REST API plugin:
   - Settings → Community Plugins → Enable "REST API"
   - Note the local URL (default: `http://localhost:27123`)

## Install

```bash
pip install obsidian-cli
# Or use the vault files directly at $OBSIDIAN_VAULT_PATH
```

## Usage

```bash
# Search notes
ls "$OBSIDIAN_VAULT_PATH" | grep -i "query"

# Create a note
cat > "$OBSIDIAN_VAULT_PATH/daily/$(date +%Y-%m-%d).md" << 'EOF'
# $(date +%Y-%m-%d)

## Tasks


## Notes
EOF

# Read a note
cat "$OBSIDIAN_VAULT_PATH/notes/topic.md"

# Search with grep
grep -r "concept" "$OBSIDIAN_VAULT_PATH" --include="*.md" -l
```

## Using the REST API

```bash
# Search notes
curl "http://localhost:27123/vault/?vault=my-vault"

# Get note content
curl "http://localhost:27123/vault/note.md?vault=my-vault"
```

## Daily Notes Workflow

```bash
# Open today's daily note (create if missing)
TODAY=$(date +%Y-%m-%d)
PATH="$OBSIDIAN_VAULT_PATH/daily/$TODAY.md"
if [ ! -f "$PATH" ]; then
  echo "# $TODAY" > "$PATH"
fi
cat "$PATH"
```
