# Client Proposal Generator — UX Design Doc

**Designer:** TBD
**Status:** Draft v0.2
**Last updated:** 2026-07-23

---

## 1. The design bet

We're betting that a clean, minimalist layout styled like an elegant document (resembling a premium letterhead or invoice) carries the trust of the proposal. We're prioritizing crisp typographic hierarchy (using a high-contrast serif for headings and a clean sans-serif for body text) and a single-screen layout with smooth scroll transition.

## 2. The defining interaction

User taps 'Generate Proposal'. The input screen transitions smoothly by fading out the textarea. The screen layout transitions into a document viewer where a clean paper document rolls up from the bottom with a gentle ease. The calculated total price ($100/hr × hours) counts up rapidly in a subtle gold/dark primary font, drawing focus to the final estimate.

## 3. Screen inventory

- **Input Screen** — Text area for notes and the primary CTA.
- **Proposal Screen** — The generated single-page client proposal document.

## 4. Screen-by-screen specs

### Input Screen

**Purpose:** To invite the user to dump raw meeting/discovery notes.

**Layout (top to bottom):**
1. Minimalist header — "Turn chaos into a proposal."
2. Massive textarea — Placeholder: "Paste your discovery call notes, meeting transcripts, or project goals..."
3. Primary button — "Generate Proposal".

**Key interactions:**
- Tap "Generate Proposal" → transitions to loading state, triggers uvicorn API request.

**States:**
- **Default:** Empty text area, disabled button.
- **Active:** Text typed/pasted, button active.
- **Loading:** Button pulses "Drafting proposal...", text area locked.

### Proposal Screen

**Purpose:** A beautifully structured web document containing the proposal details.

**Layout (top to bottom):**
1. Actions bar — "Start Over" (ghost button) and "Copy Text" (secondary button) at the top.
2. Proposal Sheet — A white, card-like document block (shadowed, bordered) containing:
   - **Header**: Project Title (e.g., "Web Development Proposal") and date.
   - **Executive Summary Section**: 1-2 paragraphs of structured summary.
   - **Scope & Deliverables Section**: Icon-bulleted lists of project deliverables.
   - **Timeline Section**: Simple milestones and expected timeframes.
   - **Investment Section**: Summary of estimated hours, hourly rate ($100/hr), and total project price.

**Key interactions:**
- Tap "Copy Text" → copies formatted plain text/markdown of the proposal to the clipboard.
- Tap "Start Over" → resets to Input Screen.

## 5. The user journey

User pastes notes and clicks "Generate Proposal." The interface slides the text input away and pulls up a beautifully typeset document page. The user scrolls down to review the Executive Summary, the deliverables, the timeline, and the calculated cost (e.g., "50 hours @ $100/hr = $5,000"). They hit "Copy Text" and paste the structured output into an email or client Slack thread.

## 6. Component & visual notes

- **Typography:** Playfair Display for the project title and section headings; Inter for body text.
- **Color:** Paper-white document background against an off-white app background. Text is deep charcoal for maximum readability. Accent elements (like bullet points or pricing totals) use a professional navy blue or emerald green.
- **Motion:** Paper document slides up from the bottom.

## 7. Accessibility & inclusion

- **Contrast:** High-contrast text on paper-white background meets WCAG AAA standards.
- **Semantic HTML:** Proper use of article, h1, h2, ul, and li tags.

## 8. What we are NOT designing

- **No client acceptance interface** — No signature boxes.
- **No multiple templates** — Single, clean default document style.

## 9. Open design questions

- [ ] Should we copy as Markdown format or rich HTML format? (Assumption: Markdown is most universal).

## 10. Handoff to engineering

The layout must transition cleanly without full page refreshes. The LLM must output clean JSON containing: title, summary, deliverables, timeline list, and estimated hours so the frontend can populate the sections and calculate the pricing.
