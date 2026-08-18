# Plan: conversational review authoring in Claude Code

Status: **done** — implemented and verified per section 4.

## Direction (decided)

Primary authoring path switches to **Claude Code, conversational**. Reviews are produced by *talking through* the book with me; I synthesize the structured markdown afterward. Reason: the issue-form workflow failed not on mechanics but on cold field-filling — Tom thinks by rambling, so the interface must be a conversation, not a form. (See memory: rambles-to-think.)

The existing GitHub issue/PR + Copilot workflow is left **intact but legacy** — not removed, not invested in further. README note can flag it later. Not touching `.github/` in this plan.

## Decisions locked

- **D1 — metadata format:** keep current H1 + bold-line markdown. No YAML, no migration. Validator passes on all 8 existing files today.
- **D2 — Format / Reading Context fields:** optional / warn-only (older files lack them; new ones should include them when the conversation surfaces them).
- **D3 — validator language:** Python 3, stdlib only.

## 1. Validator — `scripts/validate-reviews.py`

Deterministic structural checker. Runs on one file or all of `reviews/`. Exit non-zero on failure; print per-file PASS/FAIL with specific reasons. This is the feedback loop — I run it and paste real output, never assume success.

Checks per file:
- **Filename:** lowercase, hyphen-separated, `.md` (no spaces/underscores/caps).
- **Title:** line 1 is a single `# ` H1.
- **Metadata:** `**Author:**` non-empty; `**Rating:**` matches `[1-5]/5`; `**Review Date:**` is a real `YYYY-MM-DD`.
- **Sections in order:** `## Review`, `## What I Liked`, `## What I Disliked`, `## Additional Notes`.
- **Likes/Dislikes:** at least one `- ` bullet each.
- **Trailing line:** `*Review submitted via ...*`.
- **Format / Reading Context:** warn-only (per D2).

## 2. Hook — PostToolUse, deterministic

**hook vs. skill:** a *hook* because the trigger is mechanical and the check deterministic — "after any write to `reviews/*.md`, run the validator." Fires every time, no judgment.

- `PostToolUse`, matcher `Edit|Write|MultiEdit`.
- Reads tool input from stdin; if target path is under `reviews/` and ends `.md`, runs `validate-reviews.py` on it.
- On failure: exit 2 with validator output so the failure surfaces in-session.
- Wired in project `.claude/settings.json` (lives on the branch).

## 3. Skill — `write-review`, the interview

**hook vs. skill:** a *skill* because it's judgment + conversation — eliciting opinions, choosing tone/terseness, deciding what to praise. Cannot be a fixed script.

Flow the skill encodes:
1. **Ask, don't template.** Open the conversation with a few open questions (what was it, how'd you take it in — audiobook/physical/ebook, overall gut reaction). Let Tom ramble; follow threads.
2. **Probe for the balance.** Even on a 5/5, draw out at least one real gripe (his reviews always have a genuine dislike). Surface genre/trope context and any of his recurring tics if relevant.
3. **Synthesize, then confirm.** Draft the structured review in his voice (profile below), show it, let him adjust.
4. **Validate.** Write the file and let the hook (or a direct run) confirm PASS before calling it done.

### Voice profile (inferred from 8 reviews — correct anything wrong)

- First person, measured, conversational; honest but not harsh; positive default.
- Concise — `## Review` paragraph is ~2–4 sentences, no padding.
- Always balanced — even 5/5 books get a real `What I Disliked`.
- Format-aware — notes the audiobook/narration experience when relevant.
- Genre-literate — names genres/tropes plainly and judges books against their genre.
- Recurring honest tics — couldn't solve the mystery before the reveal; uneven pacing; a "smart" character who's really just lucky; romance/pervy skew beyond expectation.
- Likes/Dislikes are short phrases, not full sentences.
- Additional Notes used for reader-rec framing ("perfect for fans of X") or "No additional notes."

## 4. Verification before I report done

1. Validator on all 8 existing files → expect all PASS.
2. Deliberately broken copy (drop `## What I Disliked`) → expect FAIL with the right reason.
3. Edit a review file → confirm the hook surfaces validator output.
4. Run the skill end-to-end on one book → confirm it interviews (doesn't form-fill), output validates, voice matches.

## 5. Session goals tracking

- **Goal 1 (hook vs. skill):** validator/hook = deterministic; write-review = judgment. Narrated at each step.
- **Goal 5 (subagent):** when the skill needs book details or an "already reviewed?" check, route it to a subagent so it doesn't clutter the interview context.
