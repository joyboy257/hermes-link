---
name: github-issues
description: Manage GitHub issues from the terminal. Create, search, triage, label, and close issues. Bulk operations and automation scripts.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: [GITHUB_TOKEN]
metadata:
  hermes:
    tags: [github, issues, project-management, bug-tracking]
---

# github-issues

Full GitHub issue management from the command line.

## Setup

```bash
gh auth login
export GITHUB_TOKEN="ghp_your_token_here"
```

## Common Commands

```bash
# List issues
gh issue list --repo owner/repo --state open --limit 20
gh issue list --repo owner/repo --label bug
gh issue list --repo owner/repo --assignee @me

# View issue
gh issue view 123 --repo owner/repo

# Create issue
gh issue create --repo owner/repo --title "Bug in login" --body "Steps to reproduce..." --label bug

# Close issue
gh issue close 123 --repo owner/repo

# Add labels
gh issue edit 123 --repo owner/repo --add-label "priority:high,bug"

# Assign
gh issue edit 123 --repo owner/repo --add-assignee "username"
```

## Triage Workflow

```bash
#!/bin/bash
# triage.sh — triage new issues

REPO=$1

echo "=== Untriaged Issues ==="
gh issue list --repo "$REPO" --label "needs-triage" --state open

echo ""
echo "=== High Priority ==="
gh issue list --repo "$REPO" --label "priority:high" --state open

echo ""
echo "=== Missing Labels ==="
for issue in $(gh issue list --repo "$REPO" --state open --json number --jq '.[].number'); do
  labels=$(gh issue view "$issue" --repo "$REPO" --json labels --jq '.[].name')
  if [ -z "$labels" ]; then
    echo "Issue #$issue has no labels"
  fi
done
```

## Bulk Label Operations

```bash
# Add label to all issues matching a search
gh issue list --repo owner/repo --label "needs-review" --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --repo owner/repo --add-label "reviewed"

# Close stale issues
gh issue list --repo owner/repo --state open --search "updated:<2024-01-01" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --repo owner/repo --comment "Closing due to inactivity"
```

## Issue Templates

```bash
# Create from template
gh issue create --repo owner/repo \
  --title "Feature request" \
  --body "$(cat <<'TEMPLATE'
## Problem
Describe the problem...

## Proposed solution
Describe your solution...

## Alternatives considered
What else have you tried?
TEMPLATE
)"
```

## Milestone Tracking

```bash
# List issues by milestone
gh issue list --repo owner/repo --milestone "v1.0"

# Check milestone progress
gh api repos/owner/repo/milestones --jq '.[] | {title, open: .open_issues, closed: .closed_issues}'
```
