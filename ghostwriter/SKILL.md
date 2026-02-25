---
name: ghostwriter
description: >
  Transform AI-written documents into Jordan's polished professional voice.
  Applies a 5-phase pipeline: context extraction → AI-pattern audit (24 patterns
  from blader/humanizer) → Jordan's voice profile application → craft enhancement
  → self-audit. Output is indistinguishable from a professional human ghostwriter.
  Use when any document needs to sound like Jordan wrote it at his best.
---

# Ghostwriter Skill

Rewrite AI-generated documents in Jordan's professional voice. Zero detectable AI patterns.

## Invocation

```
/ghostwriter [text or file path]
```

Provide either:
- Raw text pasted inline
- A file path (e.g. `/path/to/draft.md`)
- A document type hint (e.g. "LinkedIn post", "client email", "technical memo")

---

## Phase 1 — Context Extraction

Before rewriting, identify:

1. **Document type**: Email / memo / LinkedIn post / report / proposal / other
2. **Audience**: Technical peer / client / investor / general
3. **Purpose**: Inform / persuade / update / pitch / connect
4. **Load voice profile**: Read `~/.claude/skills/ghostwriter/VOICE_PROFILE.md`

---

## Phase 2 — AI Pattern Audit

Scan the input for all 24 AI tells. Flag each instance.

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

## Phase 3 — Jordan's Voice Application

Load `~/.claude/skills/ghostwriter/VOICE_PROFILE.md` and apply:

### Vocabulary
- Swap AI vocabulary for Jordan's preferred words and phrases
- Enforce the anti-pattern list — if Jordan never writes it, remove it
- Use natural contractions: "I'll", "we're", "I've", "that's"
- No casual abbreviations: no lmk, tbh, fyi, btw, lol, emoji

### Structure
- Short paragraphs: 2-4 sentences
- Lists only for genuinely multi-item content — not as a default format
- No em dashes for rhythm, no mid-sentence colons for emphasis
- No Title Case on concepts

### Directness
- Remove hedging that doesn't serve a purpose
- State opinions directly — no "it could be argued that..."
- Cut filler openers — start with the substance

---

## Phase 4 — Craft Enhancement

- **Opening**: Lead with the point, not a scene-setting clause
- **Body**: Setup → insight → resolution. Cut anything that doesn't advance this.
- **Closing**: End on the actual point or a clear next step. No restatement.
- **Sentence rhythm**: Vary length — short for emphasis, longer for context. Never uniform.
- Cut ruthlessly — Jordan doesn't pad.

---

## Phase 5 — Self-Audit + Delivery

Before delivering, verify:
- [ ] Zero instances of flagged AI vocabulary (Phase 2, item 7)
- [ ] No rule-of-three stacking
- [ ] No "in conclusion" or equivalent
- [ ] Opener leads with substance
- [ ] Closer ends on the actual point
- [ ] No inline headers used decoratively
- [ ] No casual abbreviations or emoji
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

## Notes

- `VOICE_PROFILE.md` must exist — run `extract_voice_data.py` first if it's missing
- For long documents (>2000 words), rewrite section by section
- The ghostwriter's note is for Jordan only — strip it before sending to external audiences
