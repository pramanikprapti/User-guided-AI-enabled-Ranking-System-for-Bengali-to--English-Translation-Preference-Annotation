# fix_translations.py

import sqlite3
import difflib

# Path to your DB
DB_PATH = r"D:\chatbotlangchain\data\translations.db"

# Fuzzy duplicate threshold
SIMILARITY_THRESHOLD = 0.95

def keep_most_unique(translations):
    """Keep up to 5 unique translations based on fuzzy match"""
    unique = []
    for t in sorted(translations, key=lambda x: -x['score']):
        if not any(difflib.SequenceMatcher(None, t['translation'], u['translation']).ratio() > SIMILARITY_THRESHOLD for u in unique):
            unique.append(t)
        if len(unique) >= 5:
            break
    return unique

def fix_duplicates():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all unique (source_bn, reference_en)
    cur.execute("SELECT DISTINCT source_bn, reference_en FROM translations")
    pairs = cur.fetchall()

    for pair in pairs:
        source_bn = pair['source_bn']
        reference_en = pair['reference_en']

        cur.execute("""
            SELECT id, translation, score FROM translations
            WHERE source_bn = ? AND reference_en = ?
            ORDER BY score DESC
        """, (source_bn, reference_en))

        rows = cur.fetchall()
        all_translations = [{'id': row['id'], 'translation': row['translation'], 'score': row['score']} for row in rows]

        keep = keep_most_unique(all_translations)
        keep_ids = {t['id'] for t in keep}

        # Delete all rows for this pair not in keep_ids
        delete_ids = [row['id'] for row in all_translations if row['id'] not in keep_ids]
        if delete_ids:
            cur.executemany("DELETE FROM translations WHERE id = ?", [(id,) for id in delete_ids])
            print(f" Cleaned duplicates for: {source_bn[:30]}... — kept {len(keep)}, removed {len(delete_ids)}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_duplicates()
    print(" Done! Checked all stored inputs for unique translations.")
