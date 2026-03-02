import sqlite3
from pathlib import Path

DB_PATH = Path("engine.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            total_requests INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM metrics")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO metrics (total_requests) VALUES (0)"
        )

    conn.commit()
    conn.close()


def increment_requests():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE metrics SET total_requests = total_requests + 1 WHERE id = 1"
    )

    conn.commit()
    conn.close()


def get_total_requests():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT total_requests FROM metrics WHERE id = 1")
    value = cursor.fetchone()[0]

    conn.close()
    return value
