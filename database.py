import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Open a connection to tasks.db. Creates the file if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    # Row factory lets us access columns by name: row["title"] instead of row[1]
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the tasks table if it doesn't exist, and seed 3 tasks only if empty."""
    conn = get_connection()
    try:
        # Create table if missing
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Count rows FIRST — seed only if table is empty
        row_count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

        if row_count == 0:
            seed_tasks = [
                ("Learn FastAPI", 1),
                ("Build CRUD API", 0),
                ("Push to GitHub", 0),
            ]
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                seed_tasks
            )
            conn.commit()
            print(f"✅ Seeded {len(seed_tasks)} example tasks")
        else:
            print(f"ℹ️  Database already has {row_count} tasks — skipping seed")
    finally:
        conn.close()


# Run this once when module is imported (on server startup)
init_db()