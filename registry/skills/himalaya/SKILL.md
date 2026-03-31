---
name: himalaya
description: Terminal email client. Read, send, and manage email from the CLI with support for multiple accounts and GPG encryption.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: []
metadata:
  hermes:
    tags: [email, imap, smtp, cli, terminal]
---

# himalaya

Feature-rich terminal email client. Plaintext, fast, scriptable.

## Install

```bash
# From source (requires Rust)
cargo install himalaya

# Or via pip
pip install himalaya-email
```

## Setup

Create `~/.config/himalaya/config.toml`:

```toml
[[accounts]]
name = "personal"
default = true
email = "you@gmail.com"

[accounts.personal]
imap_host = "imap.gmail.com"
imap_port = 993
imap_ssl = true
smtp_host = "smtp.gmail.com"
smtp_port = 465
smtp_ssl = true
smtp_login = "you@gmail.com"
smtp_password = "your-app-password"
```

For Gmail: use an [App Password](https://support.google.com/accounts/answer/185833) (not your regular password).

## Usage

```bash
himalaya list                   # List emails (first page)
himalaya list --page 2         # Next page
himalaya read <email_id>       # Read an email
himalaya compose                # Write and send new email
himalaya search "from:boss"    # Search emails
himalaya envelope new --to "rec@example.com" --subject "Hello"
```

## Aliases for Speed

```bash
alias hl='himalaya list'
alias hr='himalaya read'
alias hs='himalaya search'
alias hc='himalaya compose'
```

## Multiple Accounts

```toml
[[accounts]]
name = "work"
email = "you@company.com"

[[accounts]]
name = "personal"
default = true
email = "you@gmail.com"
```
