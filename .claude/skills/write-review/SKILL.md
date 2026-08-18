---
name: write-review
description: Capture a book review for this repo by interviewing the user conversationally, then synthesizing a structured markdown file in their voice. Use whenever the user wants to add, write, or record a book review, or starts talking about a book they just finished.
---

# write-review

Tom thinks by talking, not by filling in fields. **Never** hand him a blank
template or a list of fields to complete. Run a conversation, then do the
structuring yourself. (See memory: rambles-to-think.)

## 1. Interview — let him ramble

Open with a couple of genuinely open questions and follow the threads he pulls
on. Do not interrogate field-by-field. Good openers:

- "What did you just finish, and what's your gut reaction?"
- "How'd you take it in — audiobook, physical, ebook?"

Let him talk. Reflect back what you heard. The fields below are *yours* to fill
from the conversation, not a checklist to read out:

- Title, author, format, reading context, overall rating (1–5)
- The actual review (his take)
- What he liked / disliked
- Any extra notes / who he'd recommend it to

## 2. Probe for the balance

His reviews are always balanced — **even a 5/5 gets a real dislike.** If he only
gushes, ask what didn't land. Listen for his recurring honest tics and draw them
out when relevant: couldn't solve the mystery before the reveal; uneven pacing;
a "smart" character who's really just lucky; a romance/pervy skew beyond what he
expected. Note the genre and judge the book against its genre's conventions.

## 3. Side-research → subagent

If you need book details (author spelling, series order) or want to check whether
he's already reviewed this book, spawn a subagent for it so the lookup doesn't
clutter the interview. Don't paste raw search dumps into the conversation.

## 4. Synthesize in his voice, then confirm

Draft the review and show it before saving. Voice:

- First person, measured, conversational; honest but not harsh; positive default.
- `## Review` is ~2–4 sentences. No padding.
- Notes the audiobook/narration experience when relevant.
- Likes/Dislikes are short phrases, not full sentences.
- Additional Notes carries reader-rec framing ("perfect for fans of X") or
  "No additional notes."

## 5. File format and validation

Filename: lowercase, hyphen-separated, `.md` (e.g. `the-tainted-cup.md`).
Structure (match existing files in `reviews/` exactly):

```markdown
# <Title>

**Author:** <Author>

**Rating:** <N>/5

**Review Date:** <YYYY-MM-DD>

**Format:** <Audiobook | Physical | eBook>

**Reading Context:** <e.g. While running, Before bed>

---

## Review

<2–4 sentences in his voice>

## What I Liked

- <phrase>

## What I Disliked

- <phrase>

## Additional Notes

<reader-rec framing, or "No additional notes.">

---

*Review submitted via [issue #N](https://github.com/atniptw/book-reviews/issues/N)*
```

Use today's date for Review Date. New reviews **should** include Format and
Reading Context (older files predate those fields). If there's no originating
issue, use `*Review submitted via Claude Code*` for the trailing line.

After writing, confirm it passes: `python3 scripts/validate-reviews.py reviews/<file>.md`.
The PostToolUse hook also runs this automatically — don't report the review done
until you've seen it PASS.
