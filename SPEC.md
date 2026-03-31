# Hermes Link — Skill Marketplace for Hermes Agent

## Overview

**Project:** hermes-link  
**Type:** Marketplace platform + Hermes integration  
**Goal:** Enable discovery, installation, and monetization of Hermes Agent skills  

## Problem

- Hermes Agent skills are scattered across the main repo and community
- No quality signaling, ratings, or curation
- No way to monetize premium skills
- Hard to discover and install skills from within Hermes chat

## Solution

A marketplace infrastructure for Hermes skills with:
1. **Registry** — Centralized skill metadata, versioning, pricing
2. **In-chat install** — Browse and install skills from Hermes CLI
3. **Quality system** — Ratings, reviews, trending, featured
4. **Monetization** — Premium skill payments (Stripe/LemonSqueezy)
5. **Developer flow** — Upload, version, update skills

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Link Platform                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Registry   │  │   Auth &     │  │  Payment    │       │
│  │   (JSON/API) │  │   Users      │  │  Gateway    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Ratings &  │  │  Discovery   │  │   Web UI     │       │
│  │   Reviews    │  │   Engine     │  │  (Optional)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Hermes Agent Integration                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  hermes-link skill — browse, install, manage from chat│   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Core Features

### 1. Skill Registry

- **Skill manifest** — JSON file with metadata:
  ```json
  {
    "id": "notion-pro",
    "name": "Notion Pro",
    "description": "Advanced Notion automation...",
    "version": "1.2.0",
    "author": {
      "id": "user-123",
      "name": "Deon",
      "url": "https://github.com/joyboy257"
    },
    "tags": ["productivity", "notion", "automation"],
    "hermes_version": ">=0.6.0",
    "prerequisites": {
      "env_vars": ["NOTION_API_KEY"],
      "pip_packages": ["notion-client"]
    },
    "pricing": {
      "type": "free|premium",
      "price_usd": 9.99,
      "license": "MIT"
    },
    "ratings": {
      "average": 4.5,
      "count": 127
    }
  }
  ```
- **Versioning** — Semver with changelog support
- **Categories** — productivity, mlops, research, devops, etc.

### 2. In-Chat Installation (Hermes Skill)

Commands:
- `/market` or `/marketplace` — Open marketplace browse
- `/market search <query>` — Search skills
- `/market install <skill-id>` — Install skill
- `/market list` — List installed
- `/market update` — Update installed skills
- `/market uninstall <skill-id>` — Remove skill

### 3. Quality System

- **Star ratings** (1-5)
- **Reviews** — Text with helpfulness votes
- **Trending** — Recent installs + ratings weight
- **Featured** — Staff-picked quality skills
- **Verified** — Author identity confirmed

### 4. Monetization

- **Free skills** — Open source, community contributions
- **Premium skills** — One-time purchase or subscription
- **Platform fee** — 15-30% depending on volume
- **Payout** — Stripe Connect or LemonSqueezy

### 5. Developer Portal

- **Upload** — Git repo URL or direct upload
- **Version** — Release new versions with changelog
- **Analytics** — Install counts, ratings, revenue
- **API keys** — For automated publishing

## Tech Stack

- **Registry:** GitHub repo with JSON manifests (simple, version-controlled)
- **API:** Optional — just fetch JSON from repo
- **Web UI:** Optional future enhancement
- **Payments:** LemonSqueezy (easier for indie devs)
- **Hermes skill:** Python + curl, pure markdown

## Phase 1 (MVP)

1. GitHub repo-based registry (JSON files in repo)
2. Basic Hermes skill for browse/search/install
3. Manual skill submission (no auto-upload yet)
4. No payments — focus on discovery first

## Phase 2

1. User accounts + authentication
2. Ratings and reviews
3. Premium skill support
4. Web dashboard

## Terms

- **ClawMart** — Working name (placeholder)
- **hermes-link** — Official repo/project name
- **Skill** — A Hermes skill package
- **Bundle** — Collection of skills

## Open Questions

- Host registry on separate GitHub repo or subfolder of hermes-link?
- Self-hosted or managed? (Starting simple with GitHub JSON)
- Payment platform — Stripe vs LemonSqueezy?
- How to handle skill updates from marketplace?

## References

- Hermes skills: `~/.hermes/hermes-agent/skills/`
- Skill format: SKILL.md with YAML frontmatter
- Skills system: `agent/skill_utils.py`