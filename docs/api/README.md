# API Reference

> This directory contains API documentation for hermes-link services.

## Endpoints

### Registry API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/skills` | List all skills |
| GET | `/api/skills/:id` | Get skill details |
| GET | `/api/skills/:id/download` | Download skill archive |
| GET | `/api/categories` | List categories |
| GET | `/api/search?q=<query>` | Search skills |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/github` | Initiate GitHub OAuth |
| GET | `/auth/github/callback` | OAuth callback |
| GET | `/auth/logout` | Logout |

### Developer API (Future)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/developer/skills` | Submit new skill |
| PUT | `/api/developer/skills/:id` | Update skill |
| DELETE | `/api/developer/skills/:id` | Delete skill |
| GET | `/api/developer/analytics` | Get analytics |

---

## Response Formats

### Skill List Response

```json
{
  "skills": [
    {
      "id": "notion-pro",
      "name": "Notion Pro",
      "description": "Advanced Notion automation...",
      "version": "1.2.0",
      "author": {
        "name": "Deon",
        "url": "https://github.com/joyboy257"
      },
      "category": "productivity",
      "tags": ["notion", "automation"],
      "pricing": {
        "type": "free"
      },
      "ratings": {
        "average": 4.5,
        "count": 127
      },
      "downloads": 1234
    }
  ],
  "total": 50,
  "page": 1,
  "per_page": 20
}
```

### Error Response

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Skill not found",
    "details": {}
  }
}
```

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| GET /api/skills | 100/minute |
| GET /api/search | 60/minute |
| POST /api/developer/* | 10/minute |

---

## Versioning

The API follows semantic versioning. Current version: `v1`

Include in requests:
```
Accept: application/json
X-API-Version: v1
```