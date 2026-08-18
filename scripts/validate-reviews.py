#!/usr/bin/env python3
"""Validate book-review markdown files against the repo's structure.

Usage:
    validate-reviews.py [FILE ...]   # validate specific files
    validate-reviews.py              # validate all of reviews/*.md

Exit code 0 if every file passes (warnings allowed), 1 if any file fails.
Checks the H1 + bold-metadata format the repo actually uses (no YAML).
"""

import datetime
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEWS_DIR = REPO_ROOT / "reviews"

REQUIRED_SECTIONS = [
    "## Review",
    "## What I Liked",
    "## What I Disliked",
    "## Additional Notes",
]
BULLET_SECTIONS = {"## What I Liked", "## What I Disliked"}

FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
AUTHOR_RE = re.compile(r"^\*\*Author:\*\*\s*(.+\S)\s*$", re.MULTILINE)
RATING_RE = re.compile(r"^\*\*Rating:\*\*\s*([1-5])/5\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^\*\*Review Date:\*\*\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
SUBMITTED_RE = re.compile(r"^\*Review submitted via .+\*$", re.MULTILINE)
FORMAT_RE = re.compile(r"^\*\*Format:\*\*\s*\S", re.MULTILINE)
CONTEXT_RE = re.compile(r"^\*\*Reading Context:\*\*\s*\S", re.MULTILINE)


def section_body(lines, heading):
    """Return the lines between `heading` and the next `## ` heading."""
    out = []
    capturing = False
    for line in lines:
        if line.strip() == heading:
            capturing = True
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            out.append(line)
    return out


def validate(path):
    """Return (errors, warnings) for one review file."""
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Filename
    if not FILENAME_RE.match(path.name):
        errors.append(
            f"filename {path.name!r} must be lowercase, hyphen-separated, .md "
            "(no spaces/underscores/capitals)"
        )

    # Title: first non-empty line is a single-# H1
    first = next((l for l in lines if l.strip()), "")
    if not re.match(r"^# \S", first) or first.startswith("## "):
        errors.append("first content line must be an H1 title ('# Title')")

    # Metadata
    if not AUTHOR_RE.search(text):
        errors.append("missing or empty '**Author:**' line")
    if not RATING_RE.search(text):
        errors.append("missing '**Rating:** N/5' line with N in 1-5")
    m = DATE_RE.search(text)
    if not m:
        errors.append("missing '**Review Date:** YYYY-MM-DD' line")
    else:
        try:
            datetime.date.fromisoformat(m.group(1))
        except ValueError:
            errors.append(f"review date {m.group(1)!r} is not a real date")

    # Required sections, in order
    headings = [l.strip() for l in lines if l.startswith("## ")]
    last_idx = -1
    for sec in REQUIRED_SECTIONS:
        if sec not in headings:
            errors.append(f"missing section '{sec}'")
            continue
        idx = headings.index(sec)
        if idx < last_idx:
            errors.append(f"section '{sec}' is out of order")
        last_idx = max(last_idx, idx)

    # Bullets in Likes/Dislikes
    for sec in BULLET_SECTIONS:
        if sec in headings:
            body = section_body(lines, sec)
            if not any(l.lstrip().startswith("- ") for l in body):
                errors.append(f"section '{sec}' needs at least one '- ' bullet")

    # Trailing submission line
    if not SUBMITTED_RE.search(text):
        errors.append("missing trailing '*Review submitted via ...*' line")

    # Optional fields (warn only)
    if not FORMAT_RE.search(text):
        warnings.append("no '**Format:**' line (optional, add for new reviews)")
    if not CONTEXT_RE.search(text):
        warnings.append("no '**Reading Context:**' line (optional, add for new reviews)")

    return errors, warnings


def main(argv):
    if argv:
        paths = [pathlib.Path(a) for a in argv]
    else:
        paths = sorted(REVIEWS_DIR.glob("*.md"))

    if not paths:
        print("No review files to validate.")
        return 0

    failed = 0
    for path in paths:
        errors, warnings = validate(path)
        if errors:
            failed += 1
            print(f"FAIL  {path.name}")
            for e in errors:
                print(f"        - {e}")
        else:
            print(f"PASS  {path.name}")
        for w in warnings:
            print(f"        ! {w}")

    print(f"\n{len(paths) - failed}/{len(paths)} passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
