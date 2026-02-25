---
name: ghostwriter
description: >
  Transform AI-written documents into a polished, professional human voice.
  Applies a 5-phase pipeline: context extraction → AI-pattern audit (24 patterns)
  → voice profile application → craft enhancement → self-audit.
  Output is indistinguishable from a professional human ghostwriter.
  Use when any document needs to sound like a real person wrote it at their best.
---

# Ghostwriter Skill

Strip AI patterns from any document and rewrite it in a confident, natural human voice. Works for emails, LinkedIn posts, proposals, memos, reports, and more.

## Invocation

```
/ghostwriter [text or file path]
/ghostwriter "Here's my draft..."
/ghostwriter docs/proposal.md
/ghostwriter docs/proposal.md --voice my-voice-profile.md
```

Provide either:
- Raw text pasted inline
- A file path (e.g. `/path/to/draft.md`)
- A document type hint (e.g. "LinkedIn post", "client email", "technical memo")
- An optional `--voice` flag pointing to your personal voice profile (see setup below)

---

## Phase 1 — Context Extraction

Before rewriting, identify:

1. **Document type**: Email / memo / LinkedIn post / report / proposal / other
2. **Audience**: Technical peer / client / investor / general public
3. **Purpose**: Inform / persuade / update / pitch / connect
4. **Voice profile**: If `--voice` is provided, load it. Otherwise, use universal professional defaults (Phase 3).

---

## Phase 2 — AI Pattern Audit

Scan the input for all 24 AI tells. Flag every instance before rewriting.

### Content Patterns
1. **Significance inflation** — treating minor points as revelations ("This is a game-changer", "Crucially important")
2. **Name-dropping** — citing philosophers/thinkers to add authority without substance
3. **Superficial -ing openers** — "Navigating the complexities of...", "Harnessing the power of..."
4. **Promotional language** — "state-of-the-art", "cutting-edge", "revolutionary", "transformative"
5. **Vague attribution** — "Studies show...", "Experts agree...", "Research suggests..." without specifics
6. **Formulaic challenges** — "In a world where...", "As we stand at the crossroads..."

### Language Patterns
7. **AI vocabulary** — flag every instance of: testament, landscape, delve, groundbreaking, pivotal, paramount, robust, seamless, leverage (as verb), synergy, utilize, facilitate, endeavor, commence, in terms of, it is worth noting
8. **Copula avoidance** — unnatural avoidance of "is/are/was/were" replaced with wordy constructions
9. **Negative parallelisms** — "not only X but also Y" structures stacked awkwardly
10. **Rule of three** — everything grouped in threes ("clarity, precision, and impact")
11. **Synonym cycling** — rotating between synonyms to avoid repetition (creates unnatural variety)
12. **False ranges** — "from X to Y" constructions that don't add information

### Style Patterns
13. **Em dash overuse** — more than 1-2 per document
14. **Boldface overuse** — bolding mid-sentence for emphasis on non-critical points
15. **Inline-header lists** — **Point:** explanation format throughout
16. **Title Case** — unnecessary capitalisation of concepts ("Key Takeaways", "Strategic Vision")
17. **Emojis** — in professional/formal contexts
18. **Curly/smart quotes** — inconsistent quote style

### Communication Patterns
19. **Chatbot artifacts** — "Certainly!", "Great question!", "Of course!", "I'd be happy to..."
20. **Cutoff disclaimers** — "As of my knowledge cutoff...", "I should note that..."
21. **Sycophancy** — excessive agreement, validation, and affirmation
22. **Filler phrases** — "It's important to remember that...", "At the end of the day...", "The bottom line is..."
23. **Excessive hedging** — "It could potentially be argued that perhaps..."
24. **Generic conclusions** — "In conclusion, [restate thesis]. Moving forward, [vague aspiration]."

---

## Phase 3 — Voice Application

### If a voice profile is provided (`--voice`)
Load the file and apply the writer's specific vocabulary, tone, structure preferences, and known anti-patterns.

### If no voice profile (default)
Apply universal professional writing standards:

**Vocabulary**
- Replace all flagged AI vocabulary (Phase 2, item 7) with direct, plain alternatives
- Use natural contractions: "I'll", "we're", "I've", "that's"
- No formal over-reach: avoid "utilize" (use "use"), "commence" (use "start"), "endeavor" (use "try")

**Structure**
- Short paragraphs: 2-4 sentences
- Lists only for genuinely multi-item content — not as a default format
- No em dashes for rhythm, no mid-sentence colons for emphasis
- No Title Case on concepts

**Directness**
- Remove hedging that doesn't serve a purpose
- State positions directly — no "it could be argued that..."
- Cut filler openers — start with the substance
- End with the actual point, not a restatement

---

## Phase 4 — Craft Enhancement

- **Opening**: Lead with the point, not a scene-setting clause
- **Body**: Setup → insight → resolution. Cut anything that doesn't advance this.
- **Closing**: End on the actual point or a clear next step. No restatement.
- **Sentence rhythm**: Vary length — short for emphasis, longer for context. Never uniform.
- Cut ruthlessly — padding is the enemy of credibility.

---

## Phase 5 — Self-Audit + Delivery

Before delivering, verify:
- [ ] Zero instances of flagged AI vocabulary (Phase 2, item 7)
- [ ] No rule-of-three stacking
- [ ] No "in conclusion" or equivalent
- [ ] Opener leads with substance
- [ ] Closer ends on the actual point
- [ ] No inline headers used decoratively
- [ ] Reads naturally at pace

### Output format

Deliver:
1. **The rewritten document** — clean, no commentary inline
2. **Ghostwriter's note** — 3-5 bullets: key changes made and why

Example:
```
Ghostwriter's note:
• Removed "testament to", "landscape", and "pivotal" — replaced with direct language
• Shortened opener — leads with the point, not a scene-setting clause
• Broke 3 rule-of-three structures — varied the rhythm
• Tightened conclusion — removed restatement, ended on the actual insight
• Swapped passive voice in 2 places
```

---

## Optional: Build Your Own Voice Profile

To get output that sounds specifically like *you*, create a voice profile and pass it with `--voice`.

Your voice profile should capture:

```markdown
# [Your Name] — Voice Profile

## Core Voice
[2-3 sentences describing your general communication style]

## Vocabulary
- Words/phrases you use often
- Words you never use
- Contractions: yes/no/sometimes

## Structure
- Paragraph length preference
- How you open emails/posts
- How you close them

## Tone by Context
- Professional emails: [describe]
- LinkedIn posts: [describe]
- Internal memos: [describe]

## Hard Rules
- Things you never write (e.g. "I hope this email finds you well")
- Formatting preferences (bullet points? headers? plain prose?)
```

Save it anywhere on your machine and reference it with `--voice /path/to/profile.md`.

---

## Notes

- Works on any document type: emails, LinkedIn, proposals, memos, cover letters, Slack messages, blog posts
- For long documents (>2000 words), rewrite section by section
- The ghostwriter's note is for your review — strip it before sending to external audiences
- The 24-pattern audit in Phase 2 works standalone — run it on any draft to get a plain-English list of what to fix
