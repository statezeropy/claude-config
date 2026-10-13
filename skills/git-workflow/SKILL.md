---
name: git-workflow
description: Enforce Modified GitHub Flow and Conventional Commits without Jira integration, and the release rule — the version is the GitHub Release tag, never a field in a file, created only on the user's request; date suffix _vYYMMDD for deliverables that cannot carry a release. Use when creating branches, committing changes, creating Pull Requests, or when the user asks for a release or a version.
allowed-tools: Bash
metadata:
  reviewed: 2026-10-13
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
- **GitHub Releases (`vX.Y.Z`):** the version and the production trigger. A release is created
  only when the user asks (§3).

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
   - Create a PR targeting `main`. The body is the project's `.github/pull_request_template.md`
     (copied from [templates/pull_request_template.md](templates/pull_request_template.md)) —
     it is the **definition of done** in one place: tests, QA sheet when a judgment surface
     changed, `CHANGELOG [Unreleased]`, docs in the same PR, design-doc Status, deploy notes.
     Every box is ticked or marked 해당 없음; an empty box means the PR stays open.
   - **DO NOT MERGE.** Creating the PR ends the AI's part; the user reviews and merges.
   - Do not add reviewers — this is a solo repository unless the project says otherwise.

2.4. **Enforce it with a hook, not with memory:** the `commit-msg` hook in
   `../python-standards/templates/.pre-commit-config.yaml` (`conventional-pre-commit`) rejects a
   malformed commit message locally, so the convention holds without anyone remembering it.

### 3. Release Workflow (Versioning)
*Only when the user asks for a release or a version. Nothing in this section runs on the AI's
own initiative — not a bump, not a tag, not a release.*

3.1. **The version lives in one place: the GitHub Release.** Its tag `vX.Y.Z` *is* the
   version. No file in the repository carries it — not `pyproject.toml`, not `package.json`,
   not a lockfile. Builds read the tag at build time (`python-standards` §5 for Python,
   `deployment-conventions` §Image version for Docker), so a file and its lockfile have nothing
   to drift from. `uv version`, `npm version` and hand edits of a version field are not part of
   any procedure here.

3.2. **Version bump rule:**
   - **No version given by the user → bump `Z` only.** Read the latest release
     (`gh release list --limit 1`, or `git describe --tags --abbrev=0`), increment the patch
     number, and propose that.
   - **`X` or `Y` change only when the user names the version explicitly**
     (e.g. "release 1.3.0", "major 2.0.0"). Never infer a minor or major bump from the
     commit types — a `feat:` commit does not raise `Y` on its own, and `BREAKING CHANGE:`
     does not raise `X` on its own. Point it out, then wait for the user's number.
   - First release with no tag yet: ask; do not assume `0.1.0` or `1.0.0`.

3.3. **Procedure, on the user's request:**
   1. Propose the version (3.2) and name the commit it will point at — `main` HEAD unless the
      user says otherwise.
   2. PR: move `[Unreleased]` in `CHANGELOG.md` to `## [X.Y.Z] - YYYY-MM-DD`
      ([RELEASE.md](RELEASE.md)). Nothing else changes — there is no version field to bump.
      The user merges.
   3. On the merged `main`, create the release. The user may do it in the GitHub UI; when the
      request covers it, the AI runs it with `gh`, the body cut from the CHANGELOG section
      (command in RELEASE.md):
      ```bash
      gh release create vX.Y.Z --target main --title vX.Y.Z --notes-file <(…)
      ```
      Creating the release creates the tag; `release.yml` (`on: release: [published]`) builds
      and deploys from it (`service-conventions` §CI).
   4. Never `git tag` or push a tag by hand. A tag without a release is a version without
      notes, and a tag created from a workflow's `GITHUB_TOKEN` does not trigger `release.yml`.

3.4. **Deliverables that cannot carry a release version** — an exported document, a one-off
   artifact outside a repository, anything handed over before a release exists — take a date
   suffix instead: `<name>_vYYMMDD` (`report_v261013`), `-2`, `-3` for a second build the same
   day. The date orders builds and says nothing about what changed, so an artifact that comes
   from a repository with releases still gets its CHANGELOG entry.

### 4. Emergency Hotfix Strategy
*Use this ONLY when `main` is ahead of Production and a critical bug exists in Production.*
1. Branch from the production release: `git checkout -b hotfix/v1.0.1-<bug> v1.0.0`.
2. Fix, commit (`fix:`), push the branch.
3. On the user's request, release from the branch:
   `gh release create v1.0.1 --target hotfix/v1.0.1-<bug> --notes-file <(…)` — the release
   workflow deploys it.
4. PR the fix (and its CHANGELOG entry) back to `main`.

### Checklist
Before finishing, verify:
- [ ] Working on a feature/hotfix branch (not main).
- [ ] Branch name includes Type (e.g., feat/...).
- [ ] Commit message follows `type(scope): desc` format.
- [ ] PR created for merging to `main`.
- [ ] **Stopped at PR creation** (waiting for the user to review and merge).
- [ ] No version field edited, no tag pushed; a release exists only because the user asked.

## Examples

### Branch Naming
- `feat/user-login`
- `fix/api-timeout`

### Commit Message
- `feat(auth): add login endpoint`
- `fix: resolve null pointer exception`
