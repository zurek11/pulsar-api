---
name: release
description: Semantic versioning, changelog updates, and release PRs. Use when bumping version, writing release notes, or preparing a release PR.
allowed-tools: Read, Write, Edit, Bash(uv:*), Bash(git:*), Bash(gh:*)
---

# Release & Versioning

Same conventions as pulsar-chat — fun changelogs, space-themed nicknames.

## Version Location
Version in `pyproject.toml` → `[project]` → `version = "X.Y.Z"`

## CHANGELOG Format
Same as pulsar-chat: each release gets a nickname, emojis in section headers,
human and honest tone. See pulsar-chat's release skill for the full format guide.

## Release Steps
1. Determine version bump (MAJOR/MINOR/PATCH)
2. Update `pyproject.toml` version
3. Update `CHANGELOG.md` (new section at top, with nickname)
4. Commit: `🚀 release: v0.2.0 — Nickname`
5. Create PR: `gh pr create --title "🚀 Release v0.2.0 — Nickname" --reviewer zurek11`
6. After merge: Adam tags `git tag v0.2.0 && git push origin v0.2.0`
