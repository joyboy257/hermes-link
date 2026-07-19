# hermes-link

Skill marketplace for Hermes Agent — one command to discover, install, and manage capabilities.

```
pip install hermes-link
```

```
hermes-link list                    # Browse all skills
hermes-link search <query>          # Search by name/tag/description
hermes-link info <name>             # Full skill details
hermes-link install <name>          # Install a skill
hermes-link install <name> --force  # Reinstall
hermes-link uninstall <name>        # Remove a skill
hermes-link installed               # List installed skills
hermes-link update                  # Update all skills
```

## Skills (19 available)

productivity | mlops | research | github | social-media | data-science | creative | gaming | smart-home | email | note-taking | leisure | custom | agentic-ai

Run `hermes-link list` to see all available skills.

## How It Works

hermes-link reads the registry index (`hermes-link-index.json`) which maps each skill to:
- `skill_md_path` — where the SKILL.md lives in this repo
- `install_command` — how to install (uv, curl, npm, pip, etc.)
- Metadata — name, description, category, tags, author

When you `install`, hermes-link either runs the install_command or git sparse-clones the skill path.

## Repository Structure

```
hermes-link/
├── hermes-link-index.json    # Master skill registry
├── hermes_link/             # Python CLI package
│   ├── cli.py
│   ├── registry.py
│   ├── installer.py
│   └── format.py
├── registry/skills/          # Skill definitions
│   ├── hermes-link/
│   └── notion-basic/
├── docs/
├── SPEC.md
└── README.md
```

## Registry

19 skills and growing. Contributions welcome - open a PR with a new `hermes-link-index.json` entry and a SKILL.md.

## Status

MVP complete. CLI is functional. Skills are installable.
