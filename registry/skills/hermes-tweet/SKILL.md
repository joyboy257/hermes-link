---
name: hermes-tweet
description: Native Hermes Agent X/Twitter plugin for Xquik. Search tweets, read replies, look up users, export followers, monitor tweets, and run approval-gated post, reply, and DM actions.
version: 0.1.6
author: Xquik
license: MIT
prerequisites:
  env_vars: [XQUIK_API_KEY]
metadata:
  hermes:
    tags: [twitter, x, social-media, hermes-agent, xquik, monitoring, posting]
    homepage: https://github.com/Xquik-dev/hermes-tweet
---

# Hermes Tweet

Native Hermes Agent plugin for X/Twitter automation through Xquik.

Use this skill when a Hermes Agent user asks to search Twitter/X, scrape or
search tweets, read tweet replies, look up users, export followers, monitor
tweets, post tweets or replies, send DMs, or automate approval-gated X actions.

## Install

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Set `XQUIK_API_KEY` in the Hermes runtime environment before read tools are
used. Set `HERMES_TWEET_ENABLE_ACTIONS=true` only when the user explicitly wants
posting, replies, DMs, monitors, webhooks, draws, extraction jobs, or other
write/private actions available.

## Tools

- Use `tweet_explore` first to find the correct Xquik endpoint or capability.
- Use `tweet_read` for public read-only X/Twitter endpoints after discovery.
- Use `tweet_action` only for writes, private reads, monitor creation, webhook
  management, extraction jobs, giveaway draws, or media operations after the
  user confirms the exact action.

## Safety

- Never ask for or expose API keys, passwords, cookies, signing keys, or TOTP
  secrets.
- Never pass credentials in tool arguments.
- Use only catalog-listed `/api/v1/...` endpoints returned by `tweet_explore`.
- State the endpoint, method, and payload before calling `tweet_action`.
- Do not retry writes through alternate routes after a policy, auth, or account
  state error.

## Examples

Search Twitter/X:

```json
{"query":"tweet search","method":"GET"}
```

Read tweet replies:

```json
{"query":"tweet replies","method":"GET"}
```

Post a tweet only after approval:

```json
{"query":"post tweet","include_actions":true}
```

Then call `tweet_action` with the user-approved endpoint and body.
