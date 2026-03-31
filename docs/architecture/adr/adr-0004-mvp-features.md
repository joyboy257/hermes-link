**ADR:** ADR-0004  
**Title:** MVP Feature Scope  
**Status:** Proposed  
**Date:** 2026-03-30  
**Author:** Hermes  

---

## Context

We need to define the minimum viable product (MVP) features. The goal is to ship fast with just enough to prove the concept.

Key constraints:
- Ship within 4 weeks
- Prove marketplace concept
- No payments initially (focus on discovery)
- Manual skill submissions (no automated upload)

## Decision

**MVP includes:**
1. GitHub repo-based registry with JSON manifests
2. hermes-link skill for Hermes CLI with:
   - `/market search <query>`
   - `/market install <skill-id>`
   - `/market list`
   - `/market uninstall <skill-id>`
3. 20+ seed skills from existing Hermes repo
4. Basic manifest validation (schema check)
5. Documentation (README, this PRD)
6. Initial ADR decisions (this doc)

**MVP excludes:**
- User accounts / authentication
- Ratings and reviews
- Premium / paid skills
- Developer portal (manual submission via PR)
- Web UI (future phase)
- Automated CI/CD validation

## Consequences

### Positive
- Fast to ship (2-4 weeks)
- Tests core hypothesis: users want in-chat skill install
- Easy to iterate based on feedback
- Simple to maintain

### Negative
- No quality signals (ratings) in MVP
- Manual skill submission process
- No revenue yet

### Neutral
- Can add features in phases
- No tech debt from unused features

## Alternatives Considered

| Scope | Description | Risk |
|-------|-------------|------|
| Larger MVP | Include ratings, user accounts | Too much to ship, delayed |
| Smaller MVP | Just search + install | Too minimal, no value |
| Proposed | Search + install + list + 20 skills | Right balance |

---

**Supersedes:** None  
**Related:** ADR-0001 (Registry Storage), ADR-0002 (Auth), ADR-0003 (Payments)