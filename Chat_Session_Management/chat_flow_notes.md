# Chat Flow Notes

This document collects architectural insights, LLM quirks, UX design notes, and edge case ideas as you build the chat system. It complements Section 4 of the PromptWise PRD.

---

## 1. Model Behavior & Routing

- Default to GPT-4 unless usage exceeds daily cap
- Consider switching to fast model for drafts / early queries
- Add token counter to estimate when nearing max length
- Future idea: Support user-selectable models (`/settings/chat-model`)

---

## 2. UX Details & Behavior

- Typing indicator with animation while LLM responds
- Auto-scroll to last message, unless user has manually scrolled up
- Retry option for failed LLM calls (rate limit, auth errors)
- Markdown renderer should support:
  - Code blocks (` ``` `)
  - Math (LaTeX if possible)
  - Emojis and tables

---

## 3. Session Autosave & Restoration

- Save session every 10 seconds if user is typing
- Restore last session from local/session storage if browser crashes
- If session is forked → assign new ID but preserve lineage
- Allow users to rename sessions or retag mid-flow

---

## 4. Token Management

- Display approximate token counter in sidebar or below message
- Exceeding token limit:
  - Prompt user to summarize previous messages
  - Option to trim earlier turns
- Admin analytics: track session token usage average

---

## 5. Edge Cases and Recovery

- LLM fails silently → show alert with option to retry / save and exit
- System error mid-reply → flag session as `corrupt` with rollback
- Forked from deleted prompt → label origin as `(deleted)` but allow chat
- Rate-limited guests → offer login to continue

---

## 6. Open Questions

- Should users be able to edit previous user messages?
- Can Admins export partial sessions (ongoing chats)?
- How to handle model switching mid-session?
- Offer timestamp toggle: always visible vs. only on hover?

