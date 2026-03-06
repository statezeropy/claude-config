---
name: git-workflow
description: Enforce Modified GitHub Flow and Conventional Commits without Jira integration. Use when creating branches, committing changes, or creating Pull Requests.
allowed-tools: Bash
---

# Git Workflow Guidelines

**IMPORTANT:** Always respond in Korean to the user.

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
     - `chore`: Changes to the build process or auxiliary tools (uv, git, etc)
   - **Example:** `feat(auth): implement jwt token validation`
   - **Example (No scope):** `fix: resolve database connection timeout`
   - Push to remote: `git push origin <branch-name>`

2.3. **Pull Request (STOP HERE):**
   - Create a PR targeting `main`.
   - **Assign the Team Lead as the reviewer.**
   - **DO NOT MERGE.** Wait for human review.

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
- [ ] **Stopped at PR creation** (waiting for Admin review).

## Examples

### Branch Naming
- `feat/user-login`
- `fix/api-timeout`

### Commit Message
- `feat(auth): add login endpoint`
- `fix: resolve null pointer exception`
