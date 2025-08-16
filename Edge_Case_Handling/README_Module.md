# Edge Case Handling

This module captures rare flows, fallback logic, and recovery procedures — based on Section 10 of the PRD.

---

## Features

- Handling corrupt sessions, failed exports, deleted forks
- CAPTCHA + abuse throttling
- Guardrails for accidental prompt or session loss

---

## Files

| File                        | Description                             |
|-----------------------------|-----------------------------------------|
| `edge_scenarios.md`         | Master table of edge cases              |
| `rollback_flowchart.drawio` | Logic for rolling back to previous state|
| `alerts_and_throttles.md`   | Quota abuse, CAPTCHA trigger rules      |
