---
name: twitter-tools
description: Interact with X/Twitter using the bird CLI via browser cookies (auth_token + ct0). Use for searching tweets, fetching user timelines, trending topics, engagement metrics, mentions, likes, and bookmarks. No X API key required.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [bird]
  env_vars: [AUTH_TOKEN, CT0]
metadata:
  hermes:
    tags: [twitter, x, social-media, bird-cli]
    homepage: https://github.com/steipete/bird
---

# Twitter Tools — X/Twitter via bird CLI

Use `bird` (from `@steipete/bird`) for X/Twitter interactions using browser cookie authentication. No X API developer account needed.

This skill is for:
- Searching tweets and users
- Fetching user timelines and threads
- Trending topics and news
- Mentions, likes, and bookmarks
- Account/engagement info lookup

## Install

`bird` is already installed at `~/.npm-global/bin/bird` (Node.js package `@steipete/bird`).

Verify:

```bash
bird --version
bird whoami
```

## Credentials

bird uses Twitter browser cookies (`auth_token` and `ct0`) rather than API keys.

### Option 1: Environment Variables (Recommended)

```bash
export AUTH_TOKEN="your_auth_token_here"
export CT0="your_ct0_here"
```

### Option 2: Browser Auto-Extraction

```bash
# Safari
bird --cookie-source safari whoami

# Chrome
bird --chrome-profile default whoami

# Firefox
bird --firefox-profile default-release whoami
```

### Option 3: Explicit Flags

```bash
bird --auth-token "..." --ct0 "..." whoami
```

### Getting Cookies

1. Log into x.com in your browser
2. Open DevTools (F12) → Application/Storage → Cookies → x.com
3. Copy `auth_token` and `ct0` values

### Cookie Expiry Warning

Twitter cookies expire roughly every 90 days. Re-extract or refresh when commands start returning auth errors.

### Credential Check

```bash
bird check
```

## Command Reference

### Search Tweets

```bash
# Basic search
bird search "AI agents"

# Search from specific user
bird search "from:openai"

# Search with count
bird search "from:openai" -n 5

# Full paged results
bird search "AI agents" --all --max-pages 5

# JSON output
bird search "AI agents" --json
```

### Get Tweet by ID/URL

```bash
# Read a tweet
bird read 1234567890123456789
bird read https://x.com/user/status/1234567890123456789

# Shortcut (ID only works if numeric)
bird 1234567890123456789

# JSON output
bird read 1234567890123456789 --json
```

### User Tweets / Timeline

```bash
# Get user tweets
bird user-tweets openai
bird user-tweets @openai

# Limit count
bird user-tweets openai -n 10

# Paged fetch
bird user-tweets openai -n 50 --max-pages 3

# JSON output
bird user-tweets openai --json
```

### Trending / News

```bash
# Trending topics
bird trending

# AI-curated news
bird trending --ai-only

# Specific categories
bird trending --news-only
bird trending --sports
bird trending --entertainment

# With related tweets
bird trending --with-tweets --tweets-per-item 3

# JSON output
bird trending --json
```

### Thread / Replies

```bash
# Full thread
bird thread 1234567890123456789

# Replies to a tweet
bird replies 1234567890123456789

# JSON output
bird replies 1234567890123456789 --json
```

### User Info

```bash
# Account info
bird about openai

# JSON output
bird about openai --json
```

### Mentions

```bash
# Your mentions (defaults to authenticated user)
bird mentions

# Count limit
bird mentions -n 20

# JSON output
bird mentions --json
```

### Likes / Bookmarks

```bash
# Your likes
bird likes -n 20

# Your bookmarks
bird bookmarks -n 20

# Unbookmark
bird unbookmark 1234567890123456789

# JSON output
bird likes --json
bird bookmarks --json
```

### Followers / Following

```bash
# Your followers
bird followers -n 20

# Users you follow
bird following -n 20

# Other user
bird followers openai -n 20

# JSON output
bird followers openai --json
```

### Post / Reply (Write Operations)

```bash
# Post tweet
bird tweet "Hello from bird CLI"

# With media
bird tweet "Check this out" --media /path/to/image.jpg

# Reply
bird reply 1234567890123456789 "Great post!"

# Follow user
bird follow username

# Unfollow
bird unfollow username
```

### Identity Check

```bash
bird whoami
```

## Example Workflows

### Monitor Brand Mentions

```bash
bird mentions -n 50 --json | jq '.[] | select(.text | contains("brand_name"))'
```

### Track Competitor Tweets

```bash
bird user-tweets competitor_handle -n 20 --json
```

### Find Engagement Opportunities

```bash
bird search "from:target_user has:engage" -n 10
```

### Research Trending Topics

```bash
bird trending --news-only --with-tweets -n 10
```

### Analyze Hashtag Performance

```bash
bird search "#YourHashtag" -n 100 --all | jq '. | length'
```

## Pitfalls

### Rate Limits

- Twitter applies strict rate limits per endpoint
- Use `--max-pages` to cap pagination
- Add delays between bulk operations
- If `429 Too Many Requests`, wait and retry

### Cookie Expiry

- `auth_token` and `ct0` expire ~every 90 days
- Symptoms: `401 Unauthorized`, `403 Forbidden`, or empty results
- Fix: re-extract cookies from browser or set fresh env vars

### Empty Results

- Some queries return no results (protected accounts, deleted content)
- Check query syntax: `from:username` not `@username` in search

### Tweet ID Shorthand

- `bird 1234567890` works as shorthand for `bird read 1234567890`
- Numeric IDs only — URLs need `bird read <url>`

### Media Attachments

- Max 4 images or 1 video per tweet
- Use absolute paths for `--media`

### JSON Parsing

- Always use `--json` when scripting or parsing output
- Use `jq` for field extraction in pipelines

## Verification Steps

1. Check bird is installed and accessible:
   ```bash
   bird --version
   ```

2. Verify credentials:
   ```bash
   bird whoami
   ```
   Should print your username. If not, cookies are missing or expired.

3. Test credential check:
   ```bash
   bird check
   ```

4. Quick functional tests:
   ```bash
   bird search "test" -n 3
   bird trending -n 5
   bird user-tweets openai -n 5
   ```

5. If auth errors occur:
   - Run `bird check` to see what's missing
   - Re-extract cookies from browser
   - Set `AUTH_TOKEN` and `CT0` env vars explicitly

## Notes

- bird uses Twitter's internal GraphQL API — behavior may change if Twitter updates their API
- Prefer read operations for automated workflows (less likely to hit write restrictions)
- Use `--plain` or `--no-emoji --no-color` for clean programmatic output
- Config file: `~/.config/bird/config.json5`
