# Prompt Engine

This module handles template creation, editing, approval workflows, and forking — based on Section 3 of the PromptWise PRD.

---

## 🔧 Responsibilities

- Define a consistent prompt schema
- Implement status transitions: Draft → Review → Approved → Archived
- Enable version control & prompt forking
- Store tags, ratings, variables, and ownership data

---

## 🧭 PRD Reference

- Section 3.1 – Prompt Schema
- Section 3.2 – Lifecycle States
- Section 3.3 – Forking & Ratings
- Section 3.4 – Permissions by Role

---

## Files in This Module

| File                        | Description                          |
|-----------------------------|--------------------------------------|
| `prompt_schema.json`        | Data model for each prompt object    |
| `prompt_lifecycle_flow.drawio`| Workflow from draft to published   |
| `sample_prompts.json`       | Example prompts for dev & testing    |
| `prompt_engine_todo.md`     | Implementation checklist             |
| `prompt_lifecycle_notes.md` | Notes on quirks, decisions, and edge |
