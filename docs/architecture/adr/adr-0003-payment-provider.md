**ADR:** ADR-0003  
**Title:** Payment Provider: Stripe vs LemonSqueezy  
**Status:** Proposed  
**Date:** 2026-03-30  
**Author:** Hermes  

---

## Context

We need to decide on a payment provider for premium skill sales.

Options:
1. **Stripe** — Full control, complex setup, higher fees for low volume
2. **LemonSqueezy** — Designed for indie devs, easier, handles taxes
3. **Gumroad** — Simple but higher fees, less control
4. **Paddle** — Similar to LemonSqueezy but more enterprise

Requirements:
- Support one-time purchases and subscriptions
- Handle global payments (including tax compliance)
- Easy for indie developer payouts
- Developer-friendly API

## Decision

**Option A: LemonSqueezy for payments.**

LemonSqueezy is purpose-built for indie developers:
- No setup fees, pay 5% + 50c per transaction
- Handles VAT/sales tax globally (critical for EU)
- Easy developer payouts
- Simple API and dashboard
- Works well for digital products

Stripe is more powerful but higher overhead and complexity. We'll use LemonSqueezy for MVP, can migrate later if needed.

## Consequences

### Positive
- Indie-friendly pricing (5% + 50c)
- Global tax compliance included
- Easy dashboard for developers
- Simple API integration
- Supports subscriptions

### Negative
- Less control than Stripe
- Fewer customization options
- Dependency on platform

### Neutral
- Can migrate to Stripe later if needed
- Need to monitor fees as volume grows

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Stripe | Full control, powerful | Complex, higher overhead for MVP |
| Gumroad | Very simple | Higher fees (10%), less control |
| Paddle | Enterprise features | More complex than LS |
| None (free only) | Simplest | No monetization possible |

---

**Supersedes:** None  
**Related:** ADR-0001 (Registry Storage), ADR-0004 (MVP Features)