<div align="center">

# 🗄️ Task API — Now with a Real Database

### FastAPI CRUD backed by SQLite — data survives restarts

*W3·A2 upgrade of the W2·A1 in-memory Task API*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi)]()
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite)]()
[![Storage](https://img.shields.io/badge/Storage-persistent-success)]()

</div>

---

## 🎯 What Changed From W2

**Nothing the client sees.** Same endpoints, same request/response shapes, same status codes.

**Everything under the hood:**

| Layer | W2·A1 (before) | W3·A2 (now) |
|-------|----------------|--------------|
| Storage | Python list in memory | SQLite file (`tasks.db`) |
| Survives restart? | ❌ No | ✅ Yes |
| Queries | List comprehensions | Parameterized SQL |
| Source of truth | Process memory | Disk |

Proof: your A1 curl tests pass against this version unchanged. Storage really is "just an implementation detail."

---

## 🤔 Why SQLite?

- **Zero setup.** No server to install, no daemon to start. It's a single file (`tasks.db`) on disk.
- **Perfect for one-developer projects.** Fine up to millions of rows for read-heavy workloads.
- **Standard library.** Python ships with `sqlite3` — no `pip install` needed.
- **Real SQL.** Same `SELECT`/`INSERT`/`UPDATE`/`DELETE` syntax you'd use in Postgres, so the skills transfer.
- **Perfect training ground** for the "one source of truth" idea — DB Browser and my API read the same file with no syncing.

When I'd choose Postgres instead: multi-writer workloads, apps that need a real network-accessible database, or anything with concurrent write pressure.

---

## 🚀 Quickstart

```bash
git clone https://github.com/SairajNarayankar/TaskAPI.git
cd TaskAPI
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

That's it. The database file `tasks.db` is created automatically on first startup, the `tasks` table is created if missing, and 3 example tasks are seeded — but ONLY on the very first run (verified by counting rows first).

- 🌐 API: http://localhost:8000
- 📖 Swagger UI: http://localhost:8000/docs

---

## 🗂️ Where the Database Lives

- **File:** `tasks.db` at the project root
- **Auto-created:** yes, on first server start
- **Git-ignored:** yes — every clone starts fresh
- **Schema:**

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
);
```

`done` is stored as `0/1` per SQLite convention — the API converts to `true/false` in responses.

---

## 📚 API Reference

| Method | Endpoint | Description | Success | Errors |
|--------|----------|-------------|:-------:|:------:|
| `GET` | `/` | API info | `200` | — |
| `GET` | `/health` | Liveness check | `200` | — |
| `GET` | `/tasks` | List all tasks | `200` | — |
| `GET` | `/tasks/{id}` | Get single task | `200` | `404` |
| `POST` | `/tasks` | Create task | `201` | `422` |
| `PUT` | `/tasks/{id}` | Update task | `200` | `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete task | `204` | `404` |

---

## 🧪 Persistence Proof

The moment W2 said would matter — and W3 delivers:

```bash
# 1. Create a task
$ curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" \
    -d '{"title":"This will survive"}'
{"id":4,"title":"This will survive","done":false}

# 2. Kill the server (Ctrl+C) and restart
$ uvicorn main:app --reload

# 3. Verify
$ curl http://localhost:8000/tasks
[..., {"id":4,"title":"This will survive","done":false}]
```

The task is still there. `id: 4` proves it came from disk — not re-seeded.

---

## 🔬 SQL by Hand (Stage 4)

Opening `tasks.db` in [DB Browser for SQLite](https://sqlitebrowser.org/) shows the same rows the API serves — because both read the same file.

<img width="1919" height="1079" alt="db-browser" src="https://github.com/user-attachments/assets/8545a03d-6eba-40c8-a6b5-fe9f7e442bee" />



### Example query I ran by hand

```sql
SELECT * FROM tasks WHERE done = 1;
```

Returned only the tasks marked complete — including one I'd just marked `done=true` via `PUT /tasks/1` from the API. **Same file, same data.** Ran an `UPDATE` in DB Browser, called `GET /tasks` right after — the change appeared instantly with no server restart. That's the "one source of truth" idea made concrete.

---

## 🛡️ Safety: Parameterized Queries

Every SQL query uses `?` placeholders — user input is never glued into SQL strings. This prevents SQL injection at the driver level.

```python
# ✅ Safe — value passed separately
conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))

# ❌ Never do this
conn.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
```

---

## 📝 Commit History

```
Stage 0: create SQLite database with seed
Stage 1: database read endpoints with parameterized queries
Stage 2: insert into database — data survives restart
Stage 3: update and delete with SQL
Stage 4: explored SQLite by hand — one query saved for README
Stage 5: database documentation and clean-clone verification
```

---

## 🤖 AI vs Me — Stage 6 Rematch

I built Stages 0–5 by hand. Then I hired Claude to do the same migration from a written spec.

The AI's code is quarantined in [`ai-version/`](./ai-version/). My hand-built version stays untouched.

### My prompt

```
Migrate a FastAPI in-memory CRUD task API to SQLite.

Requirements:
- Python 3.11, FastAPI, using the built-in sqlite3 module
- Database file: tasks.db, created automatically on first run
- Table 'tasks' with columns: id (INTEGER PRIMARY KEY AUTOINCREMENT), 
  title (TEXT NOT NULL), done (INTEGER 0/1)
- On startup: CREATE TABLE IF NOT EXISTS, then seed 3 example tasks 
  ONLY IF the table is currently empty (count rows first)
- 5 endpoints keep identical behavior from the in-memory version:
  - GET /tasks → list all
  - GET /tasks/{id} → single or 404
  - POST /tasks → 201 with new task, 400/422 if title empty
  - PUT /tasks/{id} → update, 200 or 404 (400 if body empty)
  - DELETE /tasks/{id} → 204 or 404
- ALL SQL uses parameterized queries (? placeholders)
- Never glue user input into SQL strings
- API response body: done should be true/false (Python bool), not 0/1
- Keep in a single main.py or split into main.py + database.py (your choice)
```

### What the AI did better

- **[Example]** Used a `with sqlite3.connect(...)` context manager instead of my manual `try/finally close()` — cleaner Python, harder to leak connections.
- **[Example]** Created an index on `done` for the filter query I hadn't optimized.

Both improvements I understand and could apply to my code in ~10 minutes.

### What the AI got wrong or silently ignored

- **[Example]** The seed function ran INSERT unconditionally — restarting the server 3 times produced 9 seed tasks instead of 3. Missed the "count first, seed only if empty" rule from my prompt.
- **[Example]** DELETE returned 200 with `{"deleted": true}` instead of 204 with empty body.
- **[Example]** Skipped parameterization on ONE query (`f"SELECT ... {id}"`) — a real SQL injection hole.

### What my prompt forgot to specify

- **[Example]** Didn't say "database file path relative to the module" — AI put `tasks.db` in the current working directory, which broke when run from a different folder.
- **[Example]** Didn't specify what `PUT` should do if only `done` is sent (should title be preserved?) — AI overwrote title with `NULL`.

### One rematch

Added to the prompt: *"Seed function must count rows and only insert if count = 0"* and *"PUT partial updates: preserve fields not sent in the body."*

Regenerated → seed multiplication fixed. Partial update fixed. Still no index, still returned 200 on DELETE — those weren't in the spec, so on the AI it went.

### The lesson

The AI's output is exactly as good as my spec. I could only catch the seed-multiplication bug because I'd already hit it once (Stage 0) and knew to look for it. **Spec + review is my job. Generation is the AI's job.** Both halves are the whole loop.

## 👤 Author

**Sairaj Narayankar** — FlyRank AI Internship, Backend Track, W3·A2
📧 alexesriri@gmail.com · 🐙 [GitHub](https://github.com/SairajNarayankar)
