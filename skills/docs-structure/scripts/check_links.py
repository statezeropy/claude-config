#!/usr/bin/env python3
"""Verify that every relative markdown link resolves to a file that exists.

Catches the failure mode of documentation restructuring: a link that still points at the
pre-move path, or a same-directory link left behind after a rename. External links
(http, https, mailto) and pure anchors are skipped; for `file.md#section` only the file
is checked.

Usage:

  check_links.py .                    # 디렉터리를 재귀 탐색
  check_links.py docs README.md       # 디렉터리와 파일을 섞어서 지정
  check_links.py . --ignore node_modules --ignore .venv

Exit status is 1 when a broken link is found, so it can gate CI.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[(?P<label>[^\]]*)\]\((?P<target>[^)\s]+?)(?P<anchor>#[^)]*)?\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "<")
DEFAULT_IGNORES = (".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build")


def markdown_files(paths: list[Path], ignores: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".md":
            found.append(path)
        elif path.is_dir():
            found.extend(
                p
                for p in path.rglob("*.md")
                if not any(part in ignores for part in p.parts)
            )
    return sorted(set(found))


def check(files: list[Path]) -> tuple[int, list[str]]:
    checked = 0
    broken: list[str] = []
    for file in files:
        try:
            text = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            broken.append(f"{file}: 읽기 실패 — {exc}")
            continue
        for match in LINK.finditer(text):
            target = match.group("target")
            if target.startswith(SKIP_PREFIXES):
                continue
            checked += 1
            resolved = (file.parent / target).resolve()
            if not resolved.exists():
                line = text[: match.start()].count("\n") + 1
                broken.append(f"{file}:{line} → {target}")
    return checked, broken


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--ignore", action="append", default=[], help="건너뛸 디렉터리 이름")
    args = parser.parse_args()

    ignores = DEFAULT_IGNORES + tuple(args.ignore)
    files = markdown_files(args.paths, ignores)
    checked, broken = check(files)

    print(f"문서 {len(files)}개 · 내부 링크 {checked}개 · 깨진 링크 {len(broken)}개")
    for item in broken:
        print(f"  ✗ {item}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
