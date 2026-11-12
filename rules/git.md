# Git and releases

Applies in every repository. The release and hotfix steps are in the `git-workflow` skill.

- Work on a branch cut from `main`, named `<type>/<short-description>` (`feat/login-api`). Do
  not commit directly to `main`; work reaches it through a PR.
- Commits follow Conventional Commits: `<type>(<scope>): <description>`, scope optional. Types:
  `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`. The
  description is written in the project's commit language (`CLAUDE.md` 언어 — Korean by
  default); type and scope stay English. The `commit-msg` hook in the `python-standards`
  templates enforces the format, so it holds without anyone remembering it.
- A PR targets `main`. Where the project has `.github/pull_request_template.md`, the body is
  that template — the definition of done in one place — with every box ticked or marked
  해당 없음.
- Creating the PR ends the AI's part by default, and the user merges. A project's `CLAUDE.md`
  may assign merging differently (for example, the AI runs the merge when the user says to);
  where it does, follow the project's rule and its merge command.
- Do not add reviewers in a solo repository.
- `CHANGELOG.md` is the single source of release notes. An entry states the impact of a
  change, not its commit title.
- **The version is the GitHub Release tag `vX.Y.Z`; no file carries it** — not `pyproject.toml`,
  not `package.json`, not a lockfile. Builds read the tag.
- Nothing about a version happens on the AI's initiative: no bump, no tag, no release. When the
  user asks for a release without naming a version, bump `Z` only. `X` or `Y` change only when
  the user names the number — a `feat:` or `BREAKING CHANGE:` commit does not raise them; point
  it out and wait.
- Never run `git tag` or push a tag by hand: a tag without a release is a version without notes.
- A deliverable that cannot carry a release version (an exported document, a one-off artifact)
  takes a date suffix: `<name>_vYYMMDD`, then `-2`, `-3` for later builds the same day.
