# Security & Access Control

Implements authentication, PIN-based promotions, role escalation, and lockout behavior per Section 6 of the PromptWise PRD.

---

## 🔐 Responsibilities

- Support login via email/password or OAuth
- Implement 2FA for Admins and SuperAdmins
- Define lockout flow for incorrect PIN entry
- Track audit logs for secure actions (role changes, PIN usage)
- Gate certain actions behind verified identity

---

## 🧭 PRD Reference

- Section 6.1 – Role Permissions
- Section 6.2 – PIN-Based Escalation
- Section 6.3 – Lockouts & Login Limits
- Section 6.4 – Audit Logs

---

## Files in This Module

| File                         | Description                             |
|------------------------------|-----------------------------------------|
| `access_flow_diagram.drawio` | Login, 2FA, PIN, role change visual      |
| `pin_lockout_logic.md`       | Lockout thresholds, retry timers         |
| `audit_log_schema.json`      | Format for tracking secure actions       |
| `auth_api_payloads.json`     | Login, token, PIN-related examples       |
| `security_todo.md`           | Implementation checklist                 |
| `access_notes.md`            | Brainstorm notes and edge case logic     |
