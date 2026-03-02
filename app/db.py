def get_total_requests():
    conn = sqlite3.connect("engine.db")
    cursor = conn.cursor()
    cursor.execute("SELECT total FROM metrics WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
