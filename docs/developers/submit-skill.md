# Developer Guide — Submitting Skills

> This guide explains how to submit your skill to the hermes-link marketplace.

---

## Prerequisites

1. A Hermes-compatible skill with `SKILL.md` file
2. A GitHub account (for verification)
3. Git installed locally

---

## Step 1: Prepare Your Skill

Ensure your skill follows the Hermes skill format:

```markdown
---
name: my-skill
description: Short description (max 500 chars)
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [tag1, tag2]
prerequisites:
  env_vars: [VAR_NAME]
---

# My Skill

Your skill documentation here...
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (kebab-case) |
| `description` | Short description (max 500 chars) |
| `version` | Semver (e.g., 1.0.0) |
| `author` | Your name or "community" |
| `license` | MIT, Apache, GPL, etc. |
| `prerequisites.env_vars` | Required environment variables |
| `prerequisites.pip_packages` | Optional pip packages |

### Optional Fields

| Field | Description |
|-------|-------------|
| `metadata.hermes.tags` | List of tags for discovery |
| `metadata.hermes.homepage` | Documentation URL |
| `prerequisites.external_tools` | External tools needed |

---

## Step 2: Create Manifest

Create a `manifest.json` file in your skill folder:

```json
{
  "id": "my-skill",
  "name": "My Skill",
  "description": "A brief description of what this skill does.",
  "long_description": "## Features\n\n- Feature 1\n- Feature 2\n\n## Use Cases\n\nUse this skill when...",
  "version": "1.0.0",
  "author": {
    "id": "your-github-username",
    "name": "Your Name",
    "url": "https://github.com/your-username",
    "verified": false
  },
  "repository": "https://github.com/your-username/your-skill-repo",
  "tags": ["automation", "productivity"],
  "category": "productivity",
  "hermes_version": ">=0.6.0",
  "platforms": ["linux", "macos"],
  "prerequisites": {
    "env_vars": ["MY_API_KEY"],
    "pip_packages": ["requests"]
  },
  "pricing": {
    "type": "free",
    "license": "MIT"
  },
  "assets": {
    "icon": "https://example.com/icon.png"
  }
}
```

---

## Step 3: Package Your Skill

Create a tar.gz archive of your skill:

```bash
tar -czvf my-skill-1.0.0.tar.gz my-skill/
```

Your archive should contain:
```
my-skill/
├── SKILL.md
├── manifest.json
└── (other files)
```

---

## Step 4: Submit Your Skill

### Option A: GitHub Pull Request

1. Fork the hermes-link registry repository
2. Add your manifest to `skills/<category>/<skill-name>.json`
3. Add your skill archive to `assets/<skill-name>-<version>.tar.gz`
4. Submit a PR with:
   - Manifest file
   - Skill archive
   - Brief description of changes

### Option B: Create an Issue

If you don't want to do a PR, create an issue with:
- Link to your skill repository
- Category and tags
- Pricing (free or premium)

---

## Step 5: Review Process

1. **Automated validation** — Schema and format checks
2. **Manual review** — Quality and safety review (1-3 days)
3. **Published** — Available in marketplace

---

## Updating Your Skill

To update:
1. Increment version in `manifest.json`
2. Create new archive with new version
3. Submit PR or update existing file

---

## Premium Skills

For premium skills, include pricing:

```json
{
  "pricing": {
    "type": "premium",
    "price_usd": 9.99,
    "license": "Custom"
  }
}
```

You'll need to set up a LemonSqueezy product and provide the link in your manifest.

---

## Support

- Discord: Join our community
- GitHub Issues: For bugs and questions
- Email: hello@hermes-link.dev (TBD)

---

**Last Updated:** 2026-03-30