# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal book-review collection. It is content, not an application — there is no build step and no package manifest. The "logic" lives in the GitHub issue template/workflows and in Claude Code config (`.claude/skills/`, `.claude/settings.json`, `scripts/`). The actual reviews are markdown files in `reviews/`.

## How a review gets created

There are two paths. Both produce the same file shape in `reviews/`.

**Primary: conversational, in Claude Code.** When the user wants to add/write/record a review, use the `write-review` skill (`.claude/skills/write-review/SKILL.md`). The user thinks by talking, not by filling in fields — the skill interviews conversationally and synthesizes the structured markdown afterward. Do not invoke this by re-deriving the format yourself; the skill encodes the interview flow and voice profile in detail.

**Legacy: GitHub issue + Copilot.** The owner opens an issue using the **Book Review** form (`.github/ISSUE_TEMPLATE/book-review.yml`), which is labeled `book-review` and auto-assigned to `copilot`. The owner comments `@copilot create a PR with a polished review in reviews/`. Copilot parses the issue fields, polishes the prose, writes a new file in `reviews/`, opens a PR, and closes the issue. This path is intact but not actively developed further.

If asked to add a review by hand outside either flow, replicate the existing file shape rather than inventing a new one.

## Review file conventions

Filename: sanitized book title — lowercase, spaces and special characters replaced with hyphens, `.md` extension (e.g. `the-pragmatic-programmer.md`).

Structure (see any file in `reviews/` for the canonical form):
- H1 = book title
- Bold metadata lines: `**Author:**`, `**Rating:**` (as `N/5`), `**Review Date:**` (`YYYY-MM-DD`)
- `---` separator
- `## Review`, `## What I Liked`, `## What I Disliked`, `## Additional Notes`
- Trailing `*Review submitted via [issue #N](...)*` line

The issue template also collects **Format** (Audiobook/Physical/eBook) and **Reading Context** — these are newer fields (added in #23) and are not yet present in older review files. New reviews should include them in the metadata block when the source issue provides them.

Commit message convention: `Add review: <Book Title>`.

## Validation

`scripts/validate-reviews.py` checks a review file against the structure above (filename shape, required metadata lines, section presence/order, bullets in Likes/Dislikes, trailing submission line). Format/Reading Context are warn-only, not errors.

```
python3 scripts/validate-reviews.py                      # validate every file in reviews/
python3 scripts/validate-reviews.py reviews/<file>.md     # validate one file
```

A PostToolUse hook (`.claude/settings.json` → `scripts/review-hook.py`) runs this automatically on every Edit/Write/MultiEdit that touches `reviews/*.md` and surfaces failures back into the session. Don't consider a review done until it PASSes — the hook usually confirms this for you, but re-run manually if unsure.

## Constraints to be aware of

- **Issues are owner-only.** `.github/workflows/protect-issues.yml` auto-closes any issue opened by someone other than the repo owner. Don't design anything that depends on third-party issues.
- Preserve the author's original tone and meaning when polishing review text; improve grammar and clarity only.
