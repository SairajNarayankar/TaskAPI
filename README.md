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

![alt text](db-browser.png.png)

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

## 👤 Author

**Sairaj Narayankar** — FlyRank AI Internship, Backend Track, W3·A2
📧 alexesriri@gmail.com · 🐙 [GitHub](https://github.com/YOUR_USERNAME)