---
name: notion
description: Manage Notion pages, databases, and blocks from the terminal. Create, search, update, and query your Notion workspace via the official API.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: [NOTION_API_KEY]
metadata:
  hermes:
    tags: [notion, productivity, notes, database, api]
---

# notion

Terminal access to your Notion workspace. No browser needed.

## Setup

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a new integration and copy the Internal Integration Token
3. Share relevant pages/databases with your integration

```bash
export NOTION_API_KEY="secret_xxxxxxxxxxxx"
```

## Usage

### Search

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search term"}' | jq '.results[] | {title: .title, id: .id}'
```

### Get a Page

```bash
curl -s "https://api.notion.com/v1/pages/PAGE_ID" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" | jq '{title: .properties.title.title[0].plain_text, id: .id}'
```

### Create a Page

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "DATABASE_ID"},
    "properties": {
      "Name": {"title": [{"text": {"content": "My New Page"}}]}
    }
  }' | jq '{id: .id, url: .url}'
```

### Create a Database Entry

```bash
curl -s -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 10}' | jq '.results[] | {title: .properties.Name.title[0].plain_text}'
```

### Update Page Content

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/PAGE_ID" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Name": {"title": [{"text": {"content": "Updated Title"}}]}}}'
```

### Add a Block to a Page

```bash
curl -s -X POST "https://api.notion.com/v1/blocks/PAGE_ID/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Section Title"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Your paragraph text here."}}]}}
    ]
  }'
```

## Python Helper

```python
import urllib.request
import json
import os

NOTION_KEY = os.environ["NOTION_API_KEY"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def notion_post(path, data):
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        data=json.dumps(data).encode(),
        headers=HEADERS,
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def notion_get(path):
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        headers=HEADERS
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# Search
results = notion_post("/search", {"query": "project notes"})
for r in results["results"]:
    print(r.get("title", "Untitled"), r["id"])

# Create page
notion_post("/pages", {
    "parent": {"database_id": "your-db-id"},
    "properties": {"Name": {"title": [{"text": {"content": "New Entry"}}]}}
})
```
