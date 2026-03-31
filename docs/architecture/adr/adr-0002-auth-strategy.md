**ADR:** ADR-0002  
**Title:** Authentication Strategy  
**Status:** Proposed  
**Date:** 2026-03-30  
**Author:** Hermes  

---

## Context

We need to decide how to authenticate users. Options:
1. **GitHub OAuth** — Use GitHub as identity provider
2. **Email/Password** — Traditional auth with email verification
3. **Magic Links** — Passwordless, email-based
4. **None (MVP)** — Skip auth for initial release

Requirements:
- Developer portal requires authentication for submissions
- Users may want to rate/review (requires identity)
- Keep it simple for MVP

## Decision

**Option A: GitHub OAuth only, skip auth for MVP marketplace browsing.**

Use GitHub OAuth for developer authentication:
- Most Hermes users already have GitHub accounts
- Easy to verify developer identity (GitHub profile link in manifest)
- No separate account management

For the Hermes skill (in-chat marketplace), don't require authentication initially. Users can browse and install without login. Auth only needed for:
- Submitting skills (developer)
- Rating/reviewing (optional, can allow anonymous with flag)

## Consequences

### Positive
- Familiar login for Hermes community
- Verified author links via GitHub profile
- Simple implementation with GitHub OAuth libraries
- Developer identity validation is implicit

### Negative
- Non-GitHub users excluded
- OAuth redirect needed for full features
- Rate limiting needs care to avoid abuse

### Neutral
- Could add email auth later
- Anonymous ratings could be allowed but less trustworthy

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Email/Password | Universal | More work, password reset flows |
| Magic Links | Passwordless, easy | Email deliverability concerns |
| None | Simplest | No way to attribute reviews |

---

**Supersedes:** None  
**Related:** ADR-0001 (Registry Storage)