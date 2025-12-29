# 📘 PromptWise

[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](https://codecov.io/gh/vivekp8/PromptWise)
[![Pre-Commit Enabled](https://img.shields.io/badge/pre--commit-enabled-blue)](https://pre-commit.com/)
[![CI](https://github.com/vivekp8/PromptWise/actions/workflows/test.yml/badge.svg)](https://github.com/vivekp8/PromptWise/actions)

## 🎯 Objective
PromptWise is a **full-stack AI interface** designed to:
- Classify user prompts into categories (e.g., question, command, statement).
- Route prompts to appropriate response modules.
- Manage user sessions for continuity and personalization.
- Collect structured feedback to improve prompt handling.
- Provide a dashboard for analytics and monitoring.

---

## 🧱 Architecture

| Layer         | Technology     | Role                                                                 |
|--------------|----------------|----------------------------------------------------------------------|
| **Frontend** | React (Vite)   | User interface for prompt input, session creation, feedback submission, and dashboard |
| **Backend**  | FastAPI        | API endpoints for classification, session management, feedback logging |
| **ML Engine**| Custom Classifier | Classifies prompts and generates responses (rule-based or ML-driven) |
| **Database** | SQLite + SQLAlchemy | Stores session data and feedback entries persistently |

---

## 🔧 Core Features

### 1. **Prompt Classification**
- Endpoint: `POST /classify`
- Input: `prompt`
- Output: `label` + `response`
- Example:
  - Prompt: *“What is Copilot?”*
  - Label: *question*
  - Response: *“Let me help you with that.”*

### 2. **Session Management**
- Endpoint: `POST /session/create` → generates `session_id`
- Endpoint: `GET /session/{session_id}` → retrieves session data
- Stored in `sessions` table with:
  - `session_id`
  - `user_id`
  - `active` status

### 3. **Feedback Logging**
- Endpoint: `POST /feedback`
- Input: `prompt`, `feedback`
- Output: `status` + `label`
- Stored in `feedback` table with:
  - `id`
  - `prompt`
  - `label`
  - `feedback`
  - `timestamp`

### 4. **Feedback Dashboard**
- Endpoint: `GET /feedback/all`
- React component `FeedbackDashboard.jsx` fetches and displays feedback
- Table columns:
  - Prompt
  - Label
  - Feedback
  - Timestamp

---

## 🚀 Workflow

1. **User enters prompt** in React UI.
2. **FastAPI backend** classifies prompt via ML classifier.
3. **Response + label** returned to frontend.
4. **User submits feedback** → logged in SQLite DB.
5. **Dashboard** fetches all feedback → displays analytics.

---

## 🔮 Extensibility

- 🔍 Add filters (by label, session ID, date)
- 📊 Add charts with [Chart.js](https://www.chartjs.org/) or [Recharts](https://recharts.org/)
- 📤 Export feedback as CSV
- 🔐 Add admin login with [React Router](https://reactrouter.com/) + JWT
- 🌐 Deploy backend to [Render](https://render.com) and frontend to [Vercel](https://vercel.com)

---

## 🛠️ Development Features

- 100% test coverage
- Pre-commit hooks for formatting and linting
- CI/CD pipeline with coverage badge
- Unicode and timezone-safe PDF generation
