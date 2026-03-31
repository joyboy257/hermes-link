---
name: notion-basic
description: Basic Notion API integration for creating and managing pages.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [notion, productivity, api]
prerequisites:
  env_vars: [NOTION_API_KEY]
---

# Notion Basic

Basic Notion API integration for creating and managing pages and databases.

## Setup

1. Get your API key from notion.so/my-integrations
2. Add to ~/.hermes/.env: `NOTION_API_KEY=your_key`
3. Share pages with your integration in Notion

## Usage

```bash
# Search Notion
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search"}'

# Create page
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"parent":{"database_id":"YOUR_DB_ID"},"properties":{"Name":{"title":[{"text":{"content":"New Page"}}}}}'
```

## Documentation

See: https://developers.notion.com