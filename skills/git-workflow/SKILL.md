---
name: git-workflow
description: The release and hotfix procedures — proposing the version, moving CHANGELOG [Unreleased], creating the GitHub Release with gh, releasing a hotfix from a branch — and the PR template to copy into a project. Use when the user asks for a release, a version, a tag or a hotfix, or when a project needs its pull request template. Branch, commit, PR and version rules themselves are always loaded from the git rule.
allowed-tools: Bash
metadata:
  reviewed: 2026-11-12
---

# Release and hotfix procedures

The rules — branch names, commit format, who merges, what a version is — are in the `git` rule
(`~/.claude/rules/git.md`) and apply without this skill. This is what to do when the user asks
for a release. Nothing here runs on the AI's own initiative.

## Release

1. Propose the version and name the commit it will point at — `main` HEAD unless the user says
   otherwise. With no version given, read the latest release (`gh release list --limit 1`, or
   `git describe --tags --abbrev=0`) and increment the patch number. With no tag yet, ask; do
   not assume `0.1.0` or `1.0.0`.
2. PR: move `[Unreleased]` in `CHANGELOG.md` to `## [X.Y.Z] - YYYY-MM-DD`
   ([RELEASE.md](RELEASE.md)). Nothing else changes — there is no version field to bump. It is
   merged as the `git` rule says.
3. On the merged `main`, create the release. The user may do it in the GitHub UI; when the
   request covers it, run it with `gh`, the body cut from the CHANGELOG section (command in
   RELEASE.md):

   ```bash
   gh release create vX.Y.Z --target main --title vX.Y.Z --notes-file <(…)
   ```

   Creating the release creates the tag; `release.yml` (`on: release: [published]`) builds and
   deploys from it. A tag created from a workflow's `GITHUB_TOKEN` does not trigger
   `release.yml`, which is one more reason not to tag by hand.

## Hotfix

Only when `main` is ahead of production and a critical bug exists in production.

1. Branch from the production release: `git checkout -b hotfix/v1.0.1-<bug> v1.0.0`.
2. Fix, commit (`fix:`), push the branch.
3. On the user's request, release from the branch:
   `gh release create v1.0.1 --target hotfix/v1.0.1-<bug> --notes-file <(…)`.
4. PR the fix and its CHANGELOG entry back to `main`.

## PR template

A new project copies [templates/pull_request_template.md](templates/pull_request_template.md)
to `.github/pull_request_template.md`.
