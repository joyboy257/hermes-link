---
name: github-code-review
description: Automated code review for GitHub pull requests. Analyze diffs, leave inline comments, flag issues, and enforce code quality standards.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: [GITHUB_TOKEN]
metadata:
  hermes:
    tags: [github, code-review, pr, git, quality]
---

# github-code-review

Automated PR reviews without the mental overhead.

## Setup

```bash
gh auth login
export GITHUB_TOKEN="ghp_your_token_here"
```

## Usage

```bash
# List open PRs
gh pr list --repo owner/repo --state open

# View PR diff
gh pr diff owner/repo 123

# Leave a review comment
gh api repos/owner/repo/issues/123/comments -f body="LGTM but consider adding tests"

# Check PR status
gh pr status
```

## Automated Review Script

```bash
#!/bin/bash
# review-pr.sh — review a PR and leave comments

REPO=$1
PR_NUM=$2

echo "Reviewing PR #$PR_NUM on $REPO..."

# Get the diff
gh pr diff "$REPO" "$PR_NUM" > /tmp/pr.diff

# Check for common issues
if grep -q "console.log" /tmp/pr.diff; then
  echo "Found console.log statements"
fi

if grep -q "TODO" /tmp/pr.diff; then
  echo "Found TODO comments"
fi

if [ $(wc -l < /tmp/pr.diff) -gt 500 ]; then
  echo "PR is large (>$((500)) lines)"
fi

# Post review
gh pr review "$PR_NUM" --repo "$REPO" --comment --body "Automated review complete. See comments inline."
```

## GitHub Actions Integration

Add to `.github/workflows/review.yml`:

```yaml
name: Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run review
        run: |
          gh pr diff ${{ github.event.pull_request.number }} > diff.txt
          # Your review logic here
```

## Review Checklist

- [ ] Tests added/updated
- [ ] No secrets committed
- [ ] No debug code (console.log, print statements)
- [ ] Error handling is present
- [ ] Documentation updated if needed
- [ ] No TODOs left in code
- [ ] PR size is reasonable (< 500 lines)
