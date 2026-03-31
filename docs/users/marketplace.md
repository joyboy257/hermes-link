# User Guide — Marketplace

> This guide explains how to use the hermes-link marketplace from within Hermes Agent.

---

## Getting Started

First, install the hermes-link skill:

```
/market install hermes-link
```

This adds the marketplace commands to your Hermes session.

---

## Commands

### Browse Marketplace

```
/market
```

Opens the marketplace browser showing:
- Featured skills
- Popular skills
- Recent additions
- Categories

### Search Skills

```
/market search <query>
```

Example:
```
/market search notion
```

Returns matching skills with:
- Name and description
- Category and tags
- Rating (if available)

### Install a Skill

```
/market install <skill-id>
```

Example:
```
/market install notion-pro
```

The skill will be:
1. Downloaded from the registry
2. Extracted to `~/.hermes/skills/<skill-id>/`
3. Prerequisites checked
4. Available immediately

### List Installed Skills

```
/market list
```

Shows all skills you've installed with their versions.

### Update Skills

```
/market update
```

Checks for updates to all installed skills and updates them.

```
/market update <skill-id>
```

Updates a specific skill.

### Uninstall a Skill

```
/market uninstall <skill-id>
```

Removes the skill from your installation.

### Get Skill Info

```
/market info <skill-id>
```

Shows detailed information about a skill:
- Full description
- Version history
- Prerequisites
- Author info

### Rate a Skill

```
/market rate <skill-id> <1-5>
```

Example:
```
/market rate notion-pro 5
```

Rates a skill from 1 to 5 stars.

---

## Troubleshooting

### "Skill not found"

The skill ID might be wrong. Use `/market search` to find the correct ID.

### "Prerequisites not met"

You need to set up required environment variables first. Check the skill's info with `/market info <skill-id>` for requirements.

### "Version mismatch"

Your Hermes version is too old. Run `hermes update` to upgrade.

### "Download failed"

Check your internet connection. Try again in a few minutes.

---

## Tips

- Use tags in search: `/market search tag:notion`
- Check `/market list` regularly to see installed skills
- Run `/market update` weekly to get new features
- Rate skills to help others discover quality skills

---

## Categories

| Category | Description |
|----------|-------------|
| productivity | Notion, Linear, email tools |
| mlops | Model training, deployment |
| research | Academic research, papers |
| devops | CI/CD, monitoring, infra |
| creative | Art, video, music generation |
| social-media | Twitter, LinkedIn tools |
| other | Miscellaneous |

---

## Support

- Issues: Report problems via GitHub
- Questions: Ask in our community (TBD)

---

**Last Updated:** 2026-03-30