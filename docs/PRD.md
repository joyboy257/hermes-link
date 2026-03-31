# Hermes Link — Product Requirements Document (PRD)

**Project:** hermes-link  
**Version:** 1.0  
**Status:** Draft  
**Date:** 2026-03-30  

---

## 1. Executive Summary

### 1.1 Vision

Build the first marketplace infrastructure for Hermes Agent skills — enabling discovery, installation, quality signaling, and monetization of Hermes skills through an in-chat experience.

### 1.2 Problem Statement

1. **Discovery Gap** — Hermes skills are scattered across the main repo, with no centralized discovery mechanism
2. **Quality Opacity** — No ratings, reviews, or quality signals to distinguish high-quality skills from "slop"
3. **Monetization Barrier** — No way for developers to monetize premium skills
4. **Installation Friction** — Manual copy-paste workflow; no one-click install from within Hermes

### 1.3 Target Users

| Persona | Description | Needs |
|---------|-------------|-------|
| **Skill Consumers** | Hermes users wanting to extend capabilities | Discover, install, trust, update skills |
| **Skill Developers** | Developers building Hermes skills | Publish, monetize, get feedback, version |
| **Enterprise Buyers** | Companies needing curated agent setups | Premium support, SLA, compliance |

### 1.4 Success Metrics

- **Q1:** 50+ skills in registry, 100+ installs via marketplace
- **Q2:** User accounts, ratings system, 10+ premium skills
- **Q3:** First revenue, developer ecosystem growth
- **Q4:** 500+ skills, $10k+ monthly GMV

---

## 2. Product Overview

### 2.1 Product Name

**hermes-link** — The Hermes Agent Skill Marketplace

### 2.2 Product Type

Platform + Integration (Marketplace infrastructure with Hermes in-chat client)

### 2.3 Core Value Proposition

> One command to discover, install, and manage Hermes skills — with quality you can trust.

### 2.4 Product Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         hermes-link Platform                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐               │
│  │  Registry   │   │   Auth      │   │  Payments   │               │
│  │  Service    │   │   Service   │   │   Service   │               │
│  └─────────────┘   └─────────────┘   └─────────────┘               │
│                                                                     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐               │
│  │  Ratings    │   │   Search    │   │   Web UI    │               │
│  │  Service    │   │   Engine    │   │  (optional) │               │
│  └─────────────┘   └─────────────┘   └─────────────┘               │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┴──────────────────┐
           │         Hermes Agent Integration     │
           │                                         │
           │  ┌─────────────────────────────────┐  │
           │  │  hermes-link Skill (in-chat)    │  │
           │  │  - /market                      │  │
           │  │  - /market search <query>      │  │
           │  │  - /market install <skill-id>  │  │
           │  │  - /market list                │  │
           │  │  - /market update              │  │
           │  │  - /market uninstall <id>      │  │
           │  └─────────────────────────────────┘  │
           └────────────────────────────────────────┘
```

---

## 3. Functional Requirements

### 3.1 Registry Service

#### 3.1.1 Skill Manifest Schema

Every skill MUST provide a `manifest.json` at root:

```json
{
  "id": "string (unique, kebab-case)",
  "name": "string (human-readable)",
  "description": "string (max 500 chars)",
  "long_description": "string (markdown, max 5000 chars)",
  "version": "string (semver, e.g. '1.2.0')",
  "author": {
    "id": "string",
    "name": "string",
    "email": "string (optional)",
    "url": "string (github profile or website)",
    "verified": "boolean"
  },
  "repository": "string (url)",
  "tags": ["string"],
  "category": "string (productivity|mlops|research|devops|creative|other)",
  "hermes_version": "string (semver range, e.g. '>=0.6.0')",
  "platforms": ["linux", "macos", "win32"],
  "prerequisites": {
    "env_vars": ["string"],
    "pip_packages": ["string"],
    "external_tools": ["string"]
  },
  "pricing": {
    "type": "free|premium|subscription",
    "price_usd": "number (optional)",
    "license": "string (MIT|Apache|GPL|Custom)",
    "trial_days": "number (optional)"
  },
  "assets": {
    "skill_archive": "string (url to .tar.gz)",
    "icon": "string (url to .png)"
  },
  "metadata": {
    "created_at": "ISO8601",
    "updated_at": "ISO8601",
    "downloads": "number",
    "ratings": {
      "average": "number (1-5)",
      "count": "number"
    }
  },
  "changelog": [
    {
      "version": "string",
      "date": "ISO8601",
      "changes": ["string"]
    }
  ]
}
```

#### 3.1.2 Registry Operations

| Operation | Description | Access |
|-----------|-------------|--------|
| `GET /skills` | List all skills with filtering | Public |
| `GET /skills/:id` | Get single skill manifest | Public |
| `GET /skills/:id/download` | Download skill archive | Public |
| `POST /skills` | Submit new skill (with auth) | Developer |
| `PUT /skills/:id` | Update skill (with auth) | Developer |
| `DELETE /skills/:id` | Remove skill (with auth) | Developer |
| `GET /categories` | List categories | Public |
| `GET /search` | Search skills | Public |

#### 3.1.3 Filtering & Sorting

- **By category:** `?category=mlops`
- **By tag:** `?tag=notion`
- **By pricing:** `?pricing=free|premium`
- **By platform:** `?platform=linux`
- **Sort:** `?sort=downloads|rating|newest|name`

### 3.2 In-Chat Installation (Hermes Skill)

#### 3.2.1 Command Interface

| Command | Description | Example |
|---------|-------------|---------|
| `/market` or `/marketplace` | Open marketplace browser | `/market` |
| `/market search <query>` | Search skills | `/market search notion` |
| `/market install <skill-id>` | Install skill | `/market install notion-pro` |
| `/market list` | List installed skills | `/market list` |
| `/market update` | Update all installed | `/market update` |
| `/market update <skill-id>` | Update specific skill | `/market update notion-pro` |
| `/market uninstall <skill-id>` | Remove skill | `/market uninstall notion-pro` |
| `/market info <skill-id>` | Show skill details | `/market info notion-pro` |
| `/market rate <skill-id> <1-5>` | Rate a skill | `/market rate notion-pro 5` |

#### 3.2.2 User Flows

**Installing a Skill:**
```
User: /market install notion-pro
Hermes: Fetching manifest... ✓
        Downloading skill archive... ✓
        Extracting to ~/.hermes/skills/notion-pro/
        Installing prerequisites... ✓
        Notion Pro installed successfully!

        Next steps:
        - Set NOTION_API_KEY in ~/.hermes/.env
        - Run /skills to see available commands
```

**Updating Skills:**
```
User: /market update
Hermes: Checking for updates...
        notion-pro: 1.2.0 → 1.3.0 [NEW]
        mlops-training: up to date
        Updating notion-pro... ✓
        Done!
```

#### 3.2.3 Error Handling

| Scenario | Response |
|----------|----------|
| Skill not found | "Skill 'xyz' not found. Run /market search to browse." |
| Already installed | "Skill already installed. Run /market update to get latest." |
| Prerequisites missing | "Missing: NOTION_API_KEY. Set in ~/.hermes/.env first." |
| Download failed | "Download failed. Check your internet connection and try again." |
| Version mismatch | "Requires Hermes >=0.6.0. You have v0.5.0. Run 'hermes update'." |

### 3.3 Quality System

#### 3.3.1 Ratings

- 1-5 star scale
- One rating per user per skill
- Can change rating by re-rating
- Rating displayed as: `★★★★☆ 4.2 (127 reviews)`

#### 3.3.2 Reviews

- Text review (optional, max 2000 chars)
- Can upvote/downvote helpful reviews
- Sort by: newest, highest rated, most helpful

#### 3.3.3 Quality Badges

| Badge | Criteria |
|-------|----------|
| 🏆 Featured | Staff pick, high quality |
| ✅ Verified | Author identity confirmed |
| ⭐ Popular | 500+ downloads |
| 🆕 New | < 30 days old |

### 3.4 Monetization

#### 3.4.1 Pricing Models

| Model | Description |
|-------|-------------|
| **Free** | Open source, community contributed |
| **Premium** | One-time purchase, lifetime access |
| **Subscription** | Monthly/annual, includes updates |

#### 3.4.2 Platform Fee

| Tier | Monthly GMV | Platform Fee |
|------|-------------|--------------|
| Standard | < $1,000 | 30% |
| Growth | $1,000 - $10,000 | 20% |
| Scale | > $10,000 | 15% |

#### 3.4.3 Payment Flow

```
User: /market install notion-pro
Hermes: notion-pro is a premium skill ($9.99)
        [Buy Now] [Cancel]
User: Buy Now
→ Redirect to checkout (web)
→ Payment success
→ Skill auto-installs
→ License key stored
```

### 3.5 Developer Portal

#### 3.5.1 Features

- **Dashboard:** Stats, revenue, installs
- **Submit Skill:** Upload manifest + archive
- **Version Management:** Release new versions with changelog
- **Analytics:** Per-skill metrics
- **API Keys:** For CI/CD publishing

#### 3.5.2 Submission Requirements

1. Valid manifest.json
2. Skill archive (tar.gz with SKILL.md + files)
3. At least one tag
4. Compatible with >=0.4.0
5. No malicious code (sandboxed review)

---

## 4. Non-Functional Requirements

### 4.1 Performance

- Registry API response: < 200ms p95
- Skill download: < 5s for typical skill (< 10MB)
- Search latency: < 300ms p95

### 4.2 Reliability

- 99.9% uptime for registry
- Skill archives stored with redundancy
- Graceful degradation if payment service down

### 4.3 Security

- All API calls over HTTPS
- Developer auth via GitHub OAuth
- Skill code sandboxed before publishing
- No secret leakage in public manifests

### 4.4 Scalability

- Support 10,000+ skills
- Handle 1000+ concurrent installs
- CDN for skill archives

---

## 5. Technical Architecture

### 5.1 Registry Storage

**Option A (MVP):** GitHub repository with JSON files
- Simple, version-controlled
- No backend required
- GitHub Actions for validation

**Option B (Full):** PostgreSQL + API server
- Structured queries
- Better search
- User accounts

**Decision:** Start with Option A, migrate to B as needed.

### 5.2 Tech Stack

| Component | Technology |
|-----------|------------|
| Registry Storage | GitHub repo (JSON) |
| API | GitHub Pages + Cloudflare Workers OR simple server |
| Auth | GitHub OAuth |
| Payments | LemonSqueezy (easier for indie) |
| Hermes Skill | Python + curl |
| Hosting | Vercel (web), GitHub (registry) |

### 5.3 Data Model

```
User
├── id (uuid)
├── github_id
├── username
├── email
├── created_at
└── role (consumer|developer|admin)

Skill
├── id (kebab-case)
├── name
├── description
├── version
├── author_id
├── category
├── tags
├── pricing_type
├── price_usd
├── downloads
├── ratings_avg
├── ratings_count
└── created_at

Review
├── id
├── skill_id
├── user_id
├── rating (1-5)
├── text
├── helpful_count
└── created_at
```

---

## 6. Phased Roadmap

### Phase 1: MVP (Weeks 1-4)

**Goal:** Basic marketplace with manual skill submission

- [ ] Registry repo structure (JSON manifests)
- [ ] hermes-link skill for Hermes CLI
- [ ] `/market search` and `/market install`
- [ ] Basic manifest validation
- [ ] 20+ seed skills
- [ ] Documentation

**Milestone:** User can discover and install skills from chat.

### Phase 2: Quality & Users (Weeks 5-8)

**Goal:** Ratings, reviews, user accounts

- [ ] User accounts (GitHub OAuth)
- [ ] Rating system (1-5 stars)
- [ ] Review system with upvoting
- [ ] Quality badges (Featured, Verified, Popular)
- [ ] Search improvements (fuzzy, filters)
- [ ] Developer dashboard basic

**Milestone:** Quality signals exist, users can rate skills.

### Phase 3: Monetization (Weeks 9-12)

**Goal:** Payment system for premium skills

- [ ] LemonSqueezy integration
- [ ] Premium skill listings
- [ ] Checkout flow
- [ ] Developer payouts
- [ ] Revenue dashboard
- [ ] 10+ premium skills

**Milestone:** First revenue from marketplace.

### Phase 4: Scale (Weeks 13+)

**Goal:** Ecosystem growth

- [ ] API for automated publishing
- [ ] Web dashboard full features
- [ ] Analytics deep dive
- [ ] Enterprise features (SSO, SLA)
- [ ] Mobile companion app (optional)
- [ ] Partner integrations

**Milestone:** Self-sustaining marketplace ecosystem.

---

## 7. UI/UX Guidelines

### 7.1 In-Chat Experience

- **Minimal friction:** 2 clicks to install
- **Clear feedback:** Progress indicators, success/error messages
- **Helpful prompts:** Next steps after install
- **Graceful errors:** Explain what went wrong, how to fix

### 7.2 Web Dashboard (Future)

- Clean, modern aesthetic (like Vercel/Linear)
- Dark mode default
- Clear pricing display
- Responsive design

### 7.3 Communication Style

- Friendly but professional
- Clear, concise instructions
- No unnecessary technical jargon
- Emoji for personality (sparingly)

---

## 8. Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low skill adoption | High | Seed with quality skills, developer outreach |
| Competition emerges | Medium | First-mover advantage, network effects |
| Payment complexity | Medium | Start with free, add payments later |
| Hermes deprecation | High | Keep abstraction, support multiple versions |
| Security vulnerabilities | High | Sandbox review, dependency scanning |

---

## 9. Success Criteria

| Metric | Target (Q1) | Target (Q2) | Target (Q3) |
|--------|-------------|-------------|-------------|
| Skills in registry | 50 | 200 | 500 |
| Installs via marketplace | 100 | 500 | 2,000 |
| Active users | 50 | 200 | 1,000 |
| Premium skills | 0 | 10 | 50 |
| Revenue | $0 | $0 | $5,000/mo |

---

## 10. Appendix

### 10.1 Related Projects

- Hermes Agent: https://github.com/NousResearch/hermes-agent
- Hermes Skills: `~/.hermes/hermes-agent/skills/`
- Skill format: SKILL.md with YAML frontmatter

### 10.2 Terminology

| Term | Definition |
|------|------------|
| **Skill** | A Hermes Agent capability package |
| **Registry** | Central catalog of available skills |
| **Manifest** | JSON metadata describing a skill |
| **Bundle** | Collection of related skills |
| **GMV** | Gross Merchandise Value (total sales) |

### 10.3 References

- Semantic Versioning: https://semver.org/
- LemonSqueezy: https://lemonsqueezy.com/
- GitHub OAuth: https://docs.github.com/en/apps/oauth-apps/

---

**Document Status:** Draft v1.0  
**Last Updated:** 2026-03-30  
**Next Review:** After Phase 1 completion