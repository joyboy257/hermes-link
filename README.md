# hermes-link

Marketplace infrastructure for Hermes Agent skills.

## Quick Links

- [PRD](./docs/PRD.md)
- [Roadmap](./docs/roadmap.md)
- [Developer Guide](./docs/developers/submit-skill.md)
- [User Guide](./docs/users/marketplace.md)
- [API Reference](./docs/api/README.md)

## Project Structure

```
hermes-link/
├── SPEC.md                    # Project specification
├── README.md                  # This file
├── docs/
│   ├── PRD.md                 # Product Requirements Document
│   ├── roadmap.md             # Development roadmap
│   ├── api/
│   │   └── README.md          # API reference
│   ├── architecture/
│   │   └── adr/               # Architecture Decision Records
│   ├── developers/
│   │   └── submit-skill.md    # Developer guide
│   └── users/
│       └── marketplace.md     # User guide
└── (registry/ - coming soon)
```

## Status

**Phase:** MVP Development

Currently building:
- Registry repository structure
- JSON manifest schema
- Hermes CLI integration skill

## Vision

One command to discover, install, and manage Hermes skills — with quality you can trust.

## Related

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Hermes Skills](https://github.com/NousResearch/hermes-agent/tree/main/skills)