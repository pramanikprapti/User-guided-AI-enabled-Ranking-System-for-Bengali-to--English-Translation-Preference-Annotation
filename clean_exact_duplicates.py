import sqlite3

DB_PATH = r"D:\chatbotlangchain\data\translations.db"

def clean_exact_duplicates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Find duplicate rows by source_bn, reference_en, translation
    cursor.execute("""
        SELECT source_bn, reference_en, translation, COUNT(*) as cnt
        FROM translations
        GROUP BY source_bn, reference_en, translation
        HAVING cnt > 1
    """)
    duplicates = cursor.fetchall()

    total_deleted = 0

    for source_bn, reference_en, translation, cnt in duplicates:
        # Keep only 1, delete the rest
        rows_to_delete = cnt - 1
        cursor.execute("""
            DELETE FROM translations
            WHERE id IN (
                SELECT id FROM translations
                WHERE source_bn = ? AND reference_en = ? AND translation = ?
                LIMIT ?
            )
        """, (source_bn, reference_en, translation, rows_to_delete))
        total_deleted += rows_to_delete

    conn.commit()
    conn.close()

    print(f" Removed {total_deleted} exact duplicate rows!")

if __name__ == "__main__":
    clean_exact_duplicates()
