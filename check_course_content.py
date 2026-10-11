"""Lightweight consistency checks for the course repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEXT_SUFFIXES = {".md", ".html", ".py"}
FORBIDDEN = {
    "Gemini Pro 3.1": "unverified or outdated model label",
    "GPT-5.6 Sol": "unverified or outdated model label",
    "Claude Fable 5": "unverified or outdated model label",
    "Kimi K3": "unverified or outdated model label",
    "SeedDance 2.5": "unverified or outdated model label",
    "【截圖佔位】": "unfinished screenshot placeholder",
}

# "Kling O3" is intentionally retained as the name used in the dated SHOT-001
# and SHOT-002 production records. The lesson labels those records with their
# execution date and tells the instructor to recheck current capabilities by MCP.


def iter_course_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.resolve() != Path(__file__).resolve()
        and path.suffix.lower() in TEXT_SUFFIXES
        and ".git" not in path.parts
        and "node_modules" not in path.parts
    ]


def check_forbidden(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase, reason in FORBIDDEN.items():
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)}: {phrase!r} ({reason})")
    return errors


def check_local_references(files: list[Path]) -> list[str]:
    errors: list[str] = []
    markdown_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    html_pattern = re.compile(r"(?:src|href)=[\"']([^\"']+)[\"']")

    for path in files:
        text = path.read_text(encoding="utf-8")
        refs = markdown_pattern.findall(text) if path.suffix == ".md" else []
        if path.suffix == ".html":
            refs.extend(html_pattern.findall(text))

        for ref in refs:
            if ref.startswith(("http://", "https://", "data:", "mailto:", "#", "javascript:")):
                continue
            clean_ref = re.split(r"[?#]", ref, maxsplit=1)[0]
            if clean_ref and not (path.parent / clean_ref).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: missing local reference {ref!r}")
    return errors


def main() -> int:
    files = iter_course_files()
    errors = check_forbidden(files) + check_local_references(files)
    if errors:
        print("Course content check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Course content check passed ({len(files)} text files scanned).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
