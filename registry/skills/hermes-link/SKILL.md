---
name: hermes-link
description: Browse, install, and manage Hermes Agent skills from the hermes-link marketplace. Search, discover, and install quality skills with one command.
version: 1.0.1
author: hermes-link
license: MIT
metadata:
  hermes:
    homepage: https://github.com/joyboy257/hermes-link
    tags: [marketplace, skills, discovery, install, hermes-link]
prerequisites:
  env_vars: []
---

# hermes-link

The official client for the hermes-link skill marketplace. Browse and install skills directly from within Hermes.

## Quick Start

### Install hermes-link (marketplace client)

```bash
mkdir -p ~/.hermes/skills/productivity
cd ~/.hermes/skills/productivity

# Clone just the hermes-link folder from the repo
git clone --depth 1 --filter=blob:none --sparse https://github.com/joyboy257/hermes-link.git temp-repo
cd temp-repo
mv registry/skills/hermes-link ~/.hermes/skills/productivity/
cd ..
rm -rf temp-repo
```

Or manually:
```bash
# Create folder
mkdir -p ~/.hermes/skills/productivity/hermes-link

# Download SKILL.md
curl -sL "https://raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/hermes-link/SKILL.md" -o ~/.hermes/skills/productivity/hermes-link/SKILL.md

# Download manifest
curl -sL "https://raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/hermes-link/manifest.json" -o ~/.hermes/skills/productivity/hermes-link/manifest.json
```

### Install Any Skill

```bash
# Replace SKILL_ID with the skill you want (e.g., notion-basic)
SKILL_ID="notion-basic"

mkdir -p ~/.hermes/skills
cd ~/.hermes/skills

# Clone just the specific skill folder
git clone --depth 1 --filter=blob:none --sparse https://github.com/joyboy257/hermes-link.git temp-repo
cd temp-repo
mv registry/skills/$SKILL_ID ~/.hermes/skills/
cd ..
rm -rf temp-repo

if [ -f "~/.hermes/skills/$SKILL_ID/SKILL.md" ]; then
    echo "✓ Installed $SKILL_ID"
else
    echo "✗ Install failed for $SKILL_ID"
fi
```

### Step 2: Use the marketplace

Once installed, use these commands in your Hermes chat:

---

## Commands

### Browse All Skills

```bash
curl -s "https://raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/index.json"
```

### Search Skills

```bash
# Replace YOUR_SEARCH with your query (notion, github, ml, etc.)
QUERY="YOUR_SEARCH"
curl -s "https://raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/index.json" | jq --arg q "$QUERY" '[.[] | select(.name + .description + (.tags | join(" ")) | test($q; "i"))]'
```

### Install a Skill

```bash
# Replace SKILL_ID with the skill ID (e.g., notion-basic, twitter-tools)
SKILL_ID="SKILL_ID_HERE"
SKILLS_DIR="$HOME/.hermes/skills"

mkdir -p "$SKILLS_DIR"

# Download and extract
curl -sL "https://raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/$SKILL_ID/archive.tar.gz" | tar -xz -C "$SKILLS_DIR/" 2>/dev/null

if [ -d "$SKILLS_DIR/$SKILL_ID" ]; then
    echo "✓ Installed $SKILL_ID"
    echo "  Location: $SKILLS_DIR/$SKILL_ID"
else
    echo "✗ Failed to install $SKILL_ID"
    echo "  Check that the skill exists in the registry"
fi
```

### List Installed Skills

```bash
ls -la ~/.hermes/skills/ 2>/dev/null | grep "^d" | awk '{print $NF}' | grep -v "^\."
```

### Uninstall a Skill

```bash
# Replace SKILL_ID with the skill to remove
SKILL_ID="SKILL_ID_HERE"
rm -rf ~/.hermes/skills/$SKILL_ID
echo "Removed $SKILL_ID"
```

---

## Available Skills (Registry)

| ID | Name | Category | Description |
|----|------|----------|-------------|
| hermes-link | Hermes Link | productivity | Marketplace client (THIS SKILL) |
| notion-basic | Notion Basic | productivity | Basic Notion API integration |
| linear-integration | Linear Integration | productivity | Linear API for issue tracking |
| arxiv-research | ArXiv Research | research | Search academic papers |
| twitter-tools | Twitter Tools | social-media | Twitter/X research tools |
| github-workflow | GitHub Workflow | devops | Full GitHub workflow |
| whisper-transcription | Whisper Transcription | mlops | Audio transcription |
| stable-diffusion | Stable Diffusion | creative | Text-to-image generation |
| youtube-content | YouTube Content | media | Video transcript tools |
| huggingface-tools | HuggingFace Tools | mlops | Model download/upload |
| gmail-integration | Gmail Integration | productivity | Gmail API integration |

---

## Registry Location

- **Web:** github.com/joyboy257/hermes-link/tree/main/registry/skills
- **Raw Index:** raw.githubusercontent.com/joyboy257/hermes-link/main/registry/skills/index.json

---

## Support

- **Registry Issues:** github.com/joyboy257/hermes-link/issues
- **Feature Requests:** Open an issue with "feature-request" label

---

## Contributing Skills

Want to add your skill to the marketplace?

1. Fork: github.com/joyboy257/hermes-link
2. Add: Create `registry/skills/<your-skill>/manifest.json`
3. Update: Add entry to `registry/skills/index.json`
4. PR: Submit your changes

See docs/developers/submit-skill.md for full guide.