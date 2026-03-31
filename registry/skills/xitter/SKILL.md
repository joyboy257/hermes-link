---
name: xitter
description: Full X/Twitter client in your terminal. Post, browse, search, and manage your X account from the CLI.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: [X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]
metadata:
  hermes:
    tags: [twitter, x, social-media, x-cli]
---

# xitter

Terminal-native X/Twitter client. No browser needed.

## Setup

1. Create a Twitter Developer account at developer.twitter.com
2. Create a Project and App with Read and Write permissions
3. Get your API credentials from the Developer Portal
4. Export as environment variables:

```bash
export X_API_KEY="your_api_key"
export X_API_SECRET="your_api_secret"
export X_ACCESS_TOKEN="your_access_token"
export X_ACCESS_SECRET="your_access_token_secret"
```

## Install

```bash
uv tool install git+https://github.com/Infatoshi/x-cli.git
```

## Usage

```bash
xitter tweet "Hello from the terminal"
xitter timeline
xitter search "hermes agent"
xitter like <tweet_id>
xitter retweet <tweet_id>
xitter followers <username>
xitter mentions
xitter bookmarks
xitter user <username>
```

## Credentials

If you don't want to use environment variables, `xitter` will prompt for credentials on first run and store them securely.
