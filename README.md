<div align="center">

# 🎯 Task API

### A clean, in-memory CRUD REST API built with FastAPI

*Built as W2·A1 of the FlyRank AI Backend Engineering Internship*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-2094F3?style=flat)](https://www.uvicorn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

**[Live Docs](#-swagger-ui) · [Quickstart](#-quickstart) · [API Reference](#-api-reference) · [AI vs Me](#-ai-vs-me)**

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quickstart](#-quickstart)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Usage Examples](#-usage-examples)
- [Swagger UI](#-swagger-ui)
- [The Mortality Experiment](#-the-mortality-experiment)
- [AI vs Me](#-ai-vs-me)
- [Commit History](#-commit-history)
- [What I Learned](#-what-i-learned)
- [What I'd Change](#-what-id-change)
- [Author](#-author)

---

## 🎯 About

**Task API** is a minimal, well-documented REST API for managing a to-do list. It supports all four CRUD operations (Create, Read, Update, Delete), returns proper HTTP status codes, validates input, and ships with auto-generated interactive Swagger documentation.

Data lives in an **in-memory Python list** — no database, no persistence. This is intentional: it's a Week 2 assignment, and losing data on restart is a lesson, not a bug. Week 3 fixes it with a real database.

### Why this project?

- **Every backend on Earth is CRUD in a trench coat.** Master this once — every future backend feels familiar.
- **Learn HTTP semantics for real** — the right status code for the right situation, not just `200 OK` for everything.
- **Understand validation** — servers never trust clients.
- **Practice API-first thinking** — Swagger UI makes your API a product, not just code.

---

## ✨ Features

- ✅ **Full CRUD** on tasks (`GET`, `POST`, `PUT`, `DELETE`)
- ✅ **Correct HTTP status codes** — `200`, `201`, `204`, `400/422`, `404`
- ✅ **Input validation** with Pydantic — rejects empty/missing fields
- ✅ **Interactive Swagger UI** at `/docs` — try every endpoint in the browser
- ✅ **Health check endpoint** — the same pattern real companies use
- ✅ **Bonus endpoints** — `/stats`, `/reset`, filter by status
- ✅ **Zero external dependencies beyond FastAPI + Uvicorn**
- ✅ **Under 100 lines of code**

---

## 🛠 Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Language | **Python 3.11** | Modern, typed, expressive |
| Framework | **FastAPI** | Auto-docs, type safety, async-ready |
| Server | **Uvicorn** | Production-grade ASGI server |
| Validation | **Pydantic v2** | Automatic request validation from type hints |
| Docs | **Swagger UI** (built-in) | Free with FastAPI — no config needed |

---

## 🚀 Quickstart

Get running in **under 60 seconds**:

```bash
# 1. Clone the repo
git clone https://github.com/SairajNarayankar/TaskAPI.git
cd TaskAPI

# 2. Create + activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install fastapi "uvicorn[standard]"

# 4. Run the server
uvicorn main:app --reload
```

🎉 Server running at:

- 🌐 **API:** http://localhost:8000
- 📖 **Interactive Docs:** http://localhost:8000/docs
- 📄 **OpenAPI Schema:** http://localhost:8000/openapi.json

---

## 📁 Project Structure

```
TaskAPI/
├── main.py                 # Entire API — under 100 lines
├── ai-version/             # Stage 7: AI-generated version (quarantined)
│   └── main.py
├── docs/
│   ├── swagger-ui.png      # Screenshot of interactive docs
│   └── ai-diff.txt         # Diff between hand-built vs AI version
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📚 API Reference

### Endpoints Overview

| Method | Endpoint | Description | Success | Errors |
|--------|----------|-------------|:-------:|:------:|
| `GET` | `/` | API metadata | `200` | — |
| `GET` | `/health` | Liveness check | `200` | — |
| `GET` | `/tasks` | List all tasks | `200` | — |
| `GET` | `/tasks/{id}` | Get single task | `200` | `404` |
| `POST` | `/tasks` | Create task | `201` | `422` |
| `PUT` | `/tasks/{id}` | Update task | `200` | `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete task | `204` | `404` |
| `GET` | `/stats` | Task statistics | `200` | — |
| `GET` | `/tasks/filter/status?done=` | Filter by status | `200` | — |
| `POST` | `/reset` | Restore seed data | `200` | — |

### Task Schema

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "done": false
}
```

### Status Code Reference

| Code | Meaning | When It's Returned |
|:----:|---------|-------------------|
| `200` | OK | Successful GET, PUT |
| `201` | Created | Successful POST |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Invalid PUT body (no fields) |
| `404` | Not Found | Task ID doesn't exist |
| `422` | Unprocessable Entity | Invalid POST payload (missing/empty title) |

---

## 💡 Usage Examples

### Create a Task

<details open>
<summary><b>🐧 Linux / macOS (bash)</b></summary>

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

</details>

<details>
<summary><b>🪟 Windows (PowerShell)</b></summary>

PowerShell mangles `curl.exe` quotes. Use `Invoke-RestMethod` instead:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/tasks `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"title":"Buy milk"}'
```

Or use a JSON file with `curl.exe`:

```powershell
'{"title":"Buy milk"}' | Out-File -Encoding ascii -NoNewline task.json
curl.exe -i -X POST http://localhost:8000/tasks `
  -H "Content-Type: application/json" -d "@task.json"
```

</details>

**Response:**

```http
HTTP/1.1 201 Created
content-type: application/json
content-length: 47

{"id":4,"title":"Buy milk","done":false}
```

### List All Tasks

```bash
$ curl -i http://localhost:8000/tasks

HTTP/1.1 200 OK
content-type: application/json

[
  {"id":1,"title":"Learn FastAPI","done":true},
  {"id":2,"title":"Build CRUD API","done":false},
  {"id":3,"title":"Push to GitHub","done":false}
]
```

### Update a Task

```bash
$ curl -i -X PUT http://localhost:8000/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{"done":true}'

HTTP/1.1 200 OK
{"id":1,"title":"Learn FastAPI","done":true}
```

### Delete a Task

```bash
$ curl -i -X DELETE http://localhost:8000/tasks/1

HTTP/1.1 204 No Content
```

### Get Task That Doesn't Exist

```bash
$ curl -i http://localhost:8000/tasks/999

HTTP/1.1 404 Not Found
{"detail":"Task 999 not found"}
```

---

## 📖 Swagger UI

FastAPI auto-generates interactive documentation at `/docs`. Every endpoint is testable with a **"Try it out"** button — no curl, no Postman.

<div align="center">

![Swagger UI Screenshot](./docs/swagger-ui.png)

*Interactive API documentation at http://localhost:8000/docs*

</div>

### What you can do in Swagger UI:

1. See every endpoint with its expected inputs and responses
2. Click **Try it out** on any endpoint
3. Fill in the request body / path params
4. Click **Execute** and see the live response
5. Full CRUD cycle without leaving the browser

---

## 🧪 The Mortality Experiment

> *"Data lives only in memory — losing it on restart is a lesson, not a bug."*

### What happens

```bash
# 1. Start server, add a task
POST /tasks {"title": "This will die"}
→ 201 Created, id=4

# 2. Verify it exists
GET /tasks
→ [..., {"id":4, "title":"This will die", "done":false}]

# 3. Kill the server (Ctrl+C), restart it
uvicorn main:app --reload

# 4. Check again
GET /tasks
→ [3 original seed tasks] — id 4 is gone
```

### Why

All tasks live in a Python list (`tasks = [...]`) inside the server process. When the process ends, the list is garbage-collected. Nothing was ever written to disk.

**Databases exist to solve exactly this.** Next week (W2·BE-04) I containerized Postgres to give this data a real home. See [ContainerizeStack](https://github.com/YOUR_USERNAME/ContainerizeStack) for that follow-up.

---

## 🤖 AI vs Me

Stage 7 of this assignment: I built the API by hand, then hired an AI (Claude) to build the same thing from a spec. Then I reviewed its work.

The full AI-generated code lives in [`ai-version/main.py`](./ai-version/main.py) — untouched, for honest comparison.

### My prompt

> ```
> [Paste your actual prompt here — the one you wrote from memory
>  before generating the AI version.]
> ```

### What the AI did better

- **[Example]** Used `response_model` to declare response schemas — cleaner Swagger docs than mine.
- **[Example]** Extracted a `get_task_or_404()` helper instead of repeating the lookup 3 times (DRY win).

Both improvements I understand and could apply to my version in ~10 minutes.

### What the AI got wrong or silently ignored

- **[Example]** Returned `200` instead of `201` on POST — my prompt clearly said `201`.
- **[Example]** Used a `dict` keyed by id instead of the list I specified.
- **[Example]** Skipped the `400` on empty PUT body — silently accepted it.

### What my prompt forgot to specify

- **[Example]** Didn't say "don't reuse deleted ids" — AI incremented from `max(id)`, which reuses gaps.
- **[Example]** Didn't specify JSON error format — AI returned strings in some cases, dicts in others.

### The rematch

Improved prompt with the missing rules → regenerated → **[what improved, what still slipped]**.

### The Lesson

The AI's output is exactly as good as your spec.
I could only judge its code because I'd built the thing myself first.
**Spec + review is my job. Generation is the AI's job. Both halves matter.**

---

## 📝 Commit History

Following the assignment's stage-by-stage discipline — one honest commit per stage:

| # | Stage | Commit |
|:-:|-------|--------|
| 1 | Hello server | `Stage 0: hello server` |
| 2 | Root + health | `Stage 1: root and health endpoints` |
| 3 | Read endpoints | `Stage 2: read endpoints with 404` |
| 4 | Create + validate | `Stage 3: create with validation` |
| 5 | Update + delete | `Stage 4: full CRUD` |
| 6 | Swagger polish | `Stage 5: Swagger UI with tags` |
| 7 | Extras | `Extras: stats, filter, reset` |
| 8 | Publish + docs | `Stage 6: publish and docs` |
| 9 | AI rematch | `Stage 7: AI vs me` |

View: `git log --oneline`

---

## 🎓 What I Learned

**Concrete skills:**
- FastAPI's `Depends`, `HTTPException`, `Response`, path/body params
- Pydantic v2 models for automatic validation
- HTTP status code semantics — when to return what
- Reading and writing OpenAPI schemas
- Git workflow with meaningful commits per unit of work

**Deeper takeaways:**
- **CRUD is a heartbeat.** Every backend I'll ever build is this pattern, just fatter.
- **Status codes matter.** `200` for everything is a bug — machines read status codes, not response bodies.
- **The server never trusts the client.** Validation isn't polish; it's a boundary.
- **Interactive docs are a product feature.** Swagger UI turns "here's my API" into "try it right now."
- **Writing a spec is harder than writing code.** Stage 7 proved this — the AI built exactly what my prompt described, gaps and all.

---

## 🔧 What I'd Change

If I rebuilt this today:

- [ ] Use `response_model` on every endpoint for stricter Swagger types
- [ ] Extract a `get_task_or_404()` helper (DRY the lookup)
- [ ] Add `pytest` tests for the full CRUD cycle
- [ ] Return `400` consistently instead of Pydantic's default `422` (assignment purity)
- [ ] Add pagination on `GET /tasks` (`?limit=&offset=`)
- [ ] Track `created_at` and `updated_at` on every task
- [ ] Add a proper `requirements.txt` with pinned versions

None of these are dealbreakers — the current version meets every requirement. But if this were going anywhere near real users, these are the seven things standing between "passes the assignment" and "I'd defend this in a code review."

---

## 👤 Author

**Sairaj Narayankar**
Backend AI Engineering Intern @ FlyRank

- 📧 [alexesriri@gmail.com](mailto:alexesriri@gmail.com)
- 🐙 [GitHub](https://github.com/YOUR_USERNAME)
- 💼 [LinkedIn](https://linkedin.com/in/YOUR_HANDLE)

---

## 📄 License

MIT — free to use, learn from, and improve.

---

<div align="center">

**⭐ If this helped you learn FastAPI, drop a star on the repo ⭐**

*Built with ☕ and honest debugging as W2·A1 of the FlyRank AI Internship*

</div>