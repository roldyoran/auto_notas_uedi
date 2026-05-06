---
name: git-commit-conventional-enforcer
description: Execute git commits using Conventional Commits with enforcer and automatic scope inference, diff analysis, intelligent staging, and strict message formatting. Ensures clear, structured, and safe commits while excluding sensitive files.
license: MIT
allowed-tools: Bash, Read, Glob
---

# Git Commit - Conventional Commits (Simplified + Enforced)

## Overview

Create clean, semantic git commits by analyzing changes (diff) and generating standardized messages using Conventional Commits.

- Auto-detect type and scope
- Infer scope from file paths
- Generate structured commit messages
- Support intelligent staging
- Enforce English-only messages
- Prevent committing sensitive files



# Commit Format

```
<type>(<scope>)!: <description>

<summary>

Files:
- [ADD|MOD|DEL|REN] path/file.ext: short description

Refs:
- closes #123
```

If scope is unclear:

```
<type>: <description>
```

Breaking changes: add `!` after type/scope:

```
feat(api)!: change login response format
BREAKING CHANGE: login endpoint now returns user object instead of token
```

# Commit Rules

## Header

- lowercase only
- imperative mood (e.g., "add", "fix")
- max 50 characters
- no period at end
- no emojis

## Description

- concise and clear
- max 50 characters

## Summary (Body)

- optional, but recommended if 3+ files changed
- 1–3 lines (max 80 chars per line)
- explains WHAT changed

## Files Section

- REQUIRED when body exists
- MUST include ALL modified files
- use relative paths
- description: 2–5 words

Prefixes:
- [ADD] new file
- [MOD] modified file
- [DEL] deleted file
- [REN] renamed file

## References

- Optional but recommended
- Use to link issues/PRs
- Common keywords: `closes`, `fixes`, `resolves`, `refs`, `see`
- Format: `closes #123` or `closes GH-456`


## Commit Types

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `docs`     | Documentation only             |
| `style`    | Formatting/style (no logic)    |
| `refactor` | Code refactor (no feature/fix) |
| `perf`     | Performance improvement        |
| `test`     | Add/update tests               |
| `build`    | Build system/dependencies      |
| `ci`       | CI/config changes              |
| `chore`    | Maintenance/misc               |
| `revert`   | Revert commit                  |


# Scope Inference

Infer automatically from paths:

| Path | Scope |
|------|------|
| src/components, pages, views, src/ui | ui |
| src/store, composables, src/stores, src/state | state |
| src/router, routes.ts | router |
| routes, controllers, api/* | api |
| auth, middleware, src/auth | auth |
| models, migrations, prisma, schema | db |
| services, src/services | services |
| config files (.eslintrc, tsconfig, etc.) | config |
| tests, __tests__, spec | tests |
| .github, .gitlab-ci.yml | ci |
| docker, Dockerfile, docker-compose | docker |
| scripts, tools | chore |
| infra, terraform, ansible | infra |
| logs | logging |
| utils, types, src/lib, src/hooks | utils |
| package.json, package-lock.json, bun.lockb | deps |
| backend/, api/ | backend |
| frontend/, web/, client/ | frontend |
| apps/*, packages/* | monorepo |

Rules:
- same area → use scope
- multiple areas → MUST omit scope
- root files → omit scope
- files with spaces in path → wrap in quotes when staging


# Workflow

## 1. Analyze Changes
```bash
# If files are staged, use staged diff
git diff --staged

# If nothing staged, use working tree diff
git diff

# Also check status
git status --porcelain
```

## 2. Stage Files
```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Stage by pattern
git add *.test.*
git add src/components/*

# Interactive staging
git add -p
```

## 3. Generate Commit

- detect type
- infer scope
- summarize changes

## 4. Commit
```bash
git commit -m "<message>"
```



# Safety Rules

- NEVER commit:
  - `.env`, `.env.local`, `.env.*.local`
  - `credentials.json`, `secrets.json`, `config/secrets/*`
  - `*.pem`, `*.key`, `*.p12`, `*.jks`
  - `id_rsa`, `id_ed25519`, `*.secret`
  - `aws-credentials`, `gcp-key.json`
  - `*.log` files with sensitive data
  - `dump.sql`, `*.sqlite` with production data

If detected:
- EXCLUDE from staging using `.gitignore` or explicit exclusion
- DO NOT proceed with commit if only sensitive files remain
- WARN user and explain which files are blocked

- NEVER force push (`git push --force`) or destructive commands
- NEVER bypass hooks (`--no-verify`)



# Validation Checklist

Before committing:

- no secrets included
- header ≤ 50 chars
- description imperative
- scope valid or omitted
- body present if 3+ files (recommended)
- files section complete
- breaking changes marked with `!` and `BREAKING CHANGE:` footer

# Best Practices

- one logical change per commit
- keep messages short and meaningful
- use body only when needed
- group related files together
- English only
- no emojis



# Examples

## Standard commit
```
feat(api): add user login endpoint

Implement authentication with JWT support.

Files:
- [ADD] routes/auth.ts: login route
- [MOD] controllers/auth.ts: handle login
- [ADD] services/jwt.ts: token service

Refs:
- closes #42
```

## Breaking change
```
feat(auth)!: change user response format

Update user endpoint to return full profile object.

BREAKING CHANGE: /api/user now returns {id, name, email, avatar}
instead of {id, name, email}

Files:
- [MOD] routes/user.ts: update response schema
- [MOD] controllers/user.ts: return full profile

Refs:
- fixes #128
```

## Simple commit (≤2 files)
```
fix: resolve validation error in form

Files:
- [MOD] utils/validation.ts: fix email regex
```
