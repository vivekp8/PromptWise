# Chat & Session Management

Implements the live chat flow, session persistence, and metadata tracking described in Section 4 of the PromptWise Master PRD.

---

## Key Responsibilities

- Fork sessions from prompt templates
- Maintain parent–child lineage
- Support real-time input/output rendering with LLM
- Store chat histories with timestamps, tags, and tokens
- Restore or export past sessions
- Assign sessions to user roles

---

## PRD Reference: Section 4

- 4.1 Session Object Structure
- 4.2 Message Lifecycle
- 4.3 Forking & Restoration
- 4.4 Chat Permissions
- 4.5 Token Counter & Feedback Hooks

---

## Files in This Module

| File                   | Purpose                                 |
|------------------------|-----------------------------------------|
| `chat_schema.json`     | Data model for session + messages       |
| `session_flow.drawio`  | Session lifecycle from fork to export   |
| `payload_examples.json`| Sample chat payloads (frontend <-> API) |
| `todo.md`              | Open tasks per PRD                      |

---

## Contributor Notes

- Refer to `Security_Access_Control` for token + auth structure
- Export logic is built in tandem with `Export_Integration_System`
