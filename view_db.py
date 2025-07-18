# --------------------------------------------
# view_db.py
# --------------------------------------------

import sqlite3

DB_PATH = r"D:\chatbotlangchain\data\translations.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nAll rows in `inputs` table:\n")

cursor.execute("SELECT * FROM inputs ORDER BY id DESC;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
