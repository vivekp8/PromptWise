import sqlite3
import os

DB_PATH = "promptwise.db"

if not os.path.exists(DB_PATH):
    print(f"Database {DB_PATH} not found.")
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print(f"\nColumns in {table_name}:")
        for col in columns:
            print(f" - {col[1]} ({col[2]})")
    conn.close()
