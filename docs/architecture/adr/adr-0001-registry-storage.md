**ADR:** ADR-0001  
**Title:** Registry Storage: GitHub JSON vs Database  
**Status:** Proposed  
**Date:** 2026-03-30  
**Author:** Hermes  

---

## Context

We need to decide how to store the skill registry. The options are:
1. **GitHub repo with JSON files** — Simple, version-controlled, no backend
2. **Database (PostgreSQL) + API server** — Structured queries, better search, user accounts

Key requirements:
- Support skill manifests with versioning
- Enable search and filtering
- Handle 10,000+ skills eventually
- Low development overhead for MVP

## Decision

**Option A: GitHub JSON repository for MVP, migrate to database later.**

Start with a GitHub repository containing JSON manifests for each skill, served via GitHub Pages or a simple Cloudflare Worker. This gives us:
- Version control built-in
- No backend to maintain
- Easy manual submissions via PRs
- Git-based rollback capability

When complexity demands (user accounts, structured queries, better search), migrate to PostgreSQL.

## Consequences

### Positive
- Fast to ship MVP (no backend)
- Version control for skill data
- Simple PR-based submissions for developers
- Easy to fork/backup

### Negative
- No built-in search beyond GitHub's search
- Harder to do complex filtering
- Manual sync needed for download counts
- Git history gets messy with frequent updates

### Neutral
- Need to implement sync mechanism for download stats
- May need webhooks for real-time updates

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| PostgreSQL + API | Full flexibility, proper search | More dev work, needs hosting |
| Firebase | Real-time, easy auth | Vendor lock-in |
| Supabase | Open-source Firebase alternative | Learning curve |
| GitHub JSON | Simple, version-controlled | Limited query capability |

---

**Supersedes:** None  
**Related:** ADR-0004 (MVP Features)