# Client Proposal Generator — Product Design Doc

**Author:** TBD
**Status:** Draft v0.2
**Last updated:** 2026-07-23
**One-liner:** Turn your messy client discovery notes into a structured, professional single-page HTML client proposal.

---

## 1. The user & the moment

- **Who:** A freelancer or boutique agency owner who just finished a messy discovery call with a potential client.
- **When:** Right after the call ends, staring at a chaotic page of notes, transcripts, or bullet points, dreading the hour it usually takes to format them into a coherent proposal.
- **Why now:** Proposal writing is the highest-friction part of closing a deal. Freelancers often delay sending proposals because organizing the details is tedious.

## 2. The contract (I/O)

- **Input:** A single, large free-form text box for pasting raw, unstructured discovery call notes or meeting transcripts.
- **Output:** A beautifully formatted, structured client proposal webpage containing:
  - Executive Summary
  - Scope of Work & Deliverables
  - Timeline
  - Pricing (hourly rate of $100/hr based on the estimated development hours calculated by the AI)
- **The loop:** Paste notes → click generate → view, review, and copy the generated proposal text.

## 3. The magical moment

> "I just dumped my raw meeting notes, and three seconds later I have a complete, professional project proposal with deliverables, an estimated timeline, and a calculated budget ready to copy and send."

## 4. Scope: what we ARE building (v1)

- A single input screen featuring a massive, inviting text box.
- AI processing that extracts project details and structures them into Executive Summary, Deliverables, Timeline, and estimated hours.
- A results screen displaying the polished proposal on a clean, professional layout.
- A "Copy Text" button to copy the formatted proposal text (Markdown or plain text) for emailing.

## 5. Scope: what we are NOT building

- **No PDF / Document Exporting** — Outputting clean HTML proposals on screen is enough; generating downloadable files is out of scope.
- **No User Authentication & Accounts** — No user login, passwords, or saved draft history. Pure utility.
- **No E-signatures or Client Acceptance Links** — We aren't building a DocuSign competitor.
- **No Custom CRM or Lead Database Integrations** — No syncing to HubSpot, Salesforce, or Airtable.
- **No Multi-Currency / Dynamic Tax Calculators / Variable Rates** — Keep pricing fixed at $100/hour.

## 6. The signature detail

The dynamic layout transition. When the proposal is generated, the input panel slides away and the proposal document gracefully slides up like a clean sheet of paper rolling onto a desk, with smooth typography transitions highlighting the project title and calculated total.

## 7. Success: how we know it worked

- **Primary:** ≥50% of users who generate a proposal click the "Copy Text" button or generate a second proposal within a month, indicating the output is actually useful.
- **What we're NOT measuring:** Time spent in app. We want them in and out fast.

## 8. Open questions

- [ ] How does the AI estimate hours consistently for highly ambiguous project notes?
- [ ] What copy format (Markdown, rich HTML, or plain text) is most useful for users pasting into their emails or CRMs?

## 9. Handoff

- **For UX:** The proposal needs to look clean and professional, resembling an elegant, modern invoice or contract template.
- **For Eng:** Ensuring the LLM consistently returns strict JSON matching the new proposal structure and calculates realistic hours is the primary technical hurdle.
