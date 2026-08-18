#!/usr/bin/env python3
"""PostToolUse hook: validate a review file right after it's written/edited.

Reads the hook payload (JSON) from stdin. If the touched file is a
reviews/*.md file, runs validate-reviews.py on just that file. Exits 2 on
failure so the validator output is surfaced back into the session; exits 0
(silently) for any tool call that didn't touch a review file.
"""

import json
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEWS_DIR = REPO_ROOT / "reviews"
VALIDATOR = REPO_ROOT / "scripts" / "validate-reviews.py"


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    path = pathlib.Path(file_path).resolve()
    try:
        path.relative_to(REVIEWS_DIR)
    except ValueError:
        return 0  # not under reviews/, ignore
    if path.suffix != ".md" or not path.exists():
        return 0  # e.g. a deletion, or non-markdown

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        return 2
    sys.stdout.write(result.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
