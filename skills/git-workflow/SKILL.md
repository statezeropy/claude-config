---
name: git-workflow
description: Enforce Modified GitHub Flow and Conventional Commits without Jira integration. Use when creating branches, committing changes, or creating Pull Requests.
allowed-tools: Bash
metadata:
  reviewed: 2026-09-10
---

# Git Workflow Guidelines

## When to use
- **Branch Creation:** When starting new features, bug fixes, or any development work.
- **Committing Changes:** When saving work with proper commit message format.
- **Pull Request Creation:** When submitting code for review.
- **Release Management:** When tagging versions for production deployment.

## Instructions

### 1. Core Rules
- **Direct commits to `main` are PROHIBITED.**
- **`main` Branch:** Ready for Dev Server testing.
- **Tags (e.g., `v1.0.0`):** Triggers for Production Release.

### 2. Developer Workflow (AI & User)
2.1. **Start Work:**
   - Always create a feature branch from `main`.
   - Naming: `<type>/<short-description>`
   - **Types:** Use standard Conventional Commit types (feat, fix, refactor, etc.).
   - **Example:** `feat/login-api` or `fix/timeout-issue`

2.2. **Commit & Push (Conventional Commits):**
   - **Format:** `<type>(<scope>): <description>`
   - **Allowed Types:**
     - `feat`: A new feature
     - `fix`: A bug fix
     - `docs`: Documentation only changes
     - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
     - `refactor`: A code change that neither fixes a bug nor adds a feature
     - `perf`: A code change that improves performance
     - `test`: Adding missing tests or correcting existing tests
     - `build`: Changes to the build system or dependencies (uv, pyproject)
     - `ci`: Changes to CI configuration and workflows
     - `chore`: Anything else that touches no source (tooling, housekeeping)
   - **Example:** `feat(auth): implement jwt token validation`
   - **Example (No scope):** `fix: resolve database connection timeout`
   - Push to remote: `git push origin <branch-name>`

2.3. **Pull Request (STOP HERE):**
   - Create a PR targeting `main`, with a body that states what changed and how it was verified.
   - **DO NOT MERGE.** Creating the PR ends the AI's part; the user reviews and merges.
   - Do not add reviewers — this is a solo repository unless the project says otherwise.

2.4. **Enforce it with a hook, not with memory:** the `commit-msg` hook in
   `../python-standards/templates/.pre-commit-config.yaml` (`conventional-pre-commit`) rejects a
   malformed commit message locally, so the convention holds without anyone remembering it.

### 3. Release Workflow (Tagging)
*Execute this only when requested for Production Release.*
- Command: `git tag v1.0.0` -> `git push origin v1.0.0`

### 4. Emergency Hotfix Strategy
*Use this ONLY when `main` is ahead of Production and a critical bug exists in Production.*
1. Checkout the current Production tag (e.g., `v1.0.0`).
2. Create branch: `hotfix/v1.0.1-fix-bug`.
3. Fix bug, Commit (using `fix` type).
4. Create Tag `v1.0.1` and Push (Trigger Prod Deploy).
5. Cherry-pick the fix back to `main`.

### Checklist
Before finishing, verify:
- [ ] Working on a feature/hotfix branch (not main).
- [ ] Branch name includes Type (e.g., feat/...).
- [ ] Commit message follows `type(scope): desc` format.
- [ ] PR created for merging to `main`.
- [ ] **Stopped at PR creation** (waiting for the user to review and merge).

## Examples

### Branch Naming
- `feat/user-login`
- `fix/api-timeout`

### Commit Message
- `feat(auth): add login endpoint`
- `fix: resolve null pointer exception`
