import sqlite3
from datetime import datetime

DB_PATH = r"D:\chatbotlangchain\data\translations.db"

def create_inputs_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create new table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_bn TEXT NOT NULL,
            reference_en TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    print(" 'inputs' table ready.")

def insert_unique_inputs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get unique input pairs from translations
    cursor.execute("""
        SELECT DISTINCT TRIM(source_bn), TRIM(reference_en)
        FROM translations
    """)
    unique_pairs = cursor.fetchall()

    new_count = 0

    for source_bn, reference_en in unique_pairs:
        # Check if already logged
        cursor.execute("""
            SELECT 1 FROM inputs
            WHERE TRIM(source_bn) = ? AND TRIM(reference_en) = ?
        """, (source_bn, reference_en))

        exists = cursor.fetchone()
        if not exists:
            cursor.execute("""
                INSERT INTO inputs (source_bn, reference_en, created_at)
                VALUES (?, ?, ?)
            """, (source_bn, reference_en, datetime.now().isoformat()))
            new_count += 1

    conn.commit()
    conn.close()
    print(f" Done! {new_count} new input(s) stored in 'inputs' table.")

if __name__ == "__main__":
    create_inputs_table()
    insert_unique_inputs()
