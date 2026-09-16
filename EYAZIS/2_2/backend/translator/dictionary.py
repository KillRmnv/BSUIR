"""
Translation dictionary database operations.
Stores EN→FR word pairs and phrase pairs with POS tags and frequency.
Fast in-memory lookup for ~1500 common words, DB fallback for the rest.
"""
import psycopg2
import os

from translator.common_words import COMMON_WORDS


def _conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "ir_system"),
        user=os.environ.get("DB_USER", "ir_user"),
        password=os.environ.get("DB_PASSWORD", "ir_password"),
    )


def lookup(word: str, pos: str = None) -> list:
    """Find translations for a word, optionally filtered by POS.
    Order: in-memory COMMON_WORDS -> DB translation_dictionary."""
    lower = word.lower()

    # 1. Fast in-memory lookup
    if lower in COMMON_WORDS:
        fr, en_pos, fr_pos = COMMON_WORDS[lower]
        if pos is None or pos.upper() == en_pos.upper() or en_pos.startswith(pos[:2]):
            return [{"target": fr, "pos": fr_pos, "freq": 9999}]

    # 2. DB fallback
    conn = _conn()
    cur = conn.cursor()
    if pos:
        cur.execute(
            "SELECT target_word, target_pos, frequency "
            "FROM translation_dictionary "
            "WHERE LOWER(source_word) = LOWER(%s) AND LOWER(source_pos) = LOWER(%s) "
            "ORDER BY frequency DESC",
            (word, pos),
        )
    else:
        cur.execute(
            "SELECT target_word, target_pos, frequency "
            "FROM translation_dictionary "
            "WHERE LOWER(source_word) = LOWER(%s) "
            "ORDER BY frequency DESC",
            (word,),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"target": r[0], "pos": r[1], "freq": r[2]} for r in rows]


def lookup_phrase(words: tuple) -> dict:
    """Look up a multi-word phrase (tuple of lowercase words).
    Returns {target, length} or None."""
    conn = _conn()
    cur = conn.cursor()
    for length in range(len(words), 1, -1):
        phrase = " ".join(words[:length])
        cur.execute(
            "SELECT target_phrase, frequency "
            "FROM phrase_dictionary "
            "WHERE LOWER(source_phrase) = LOWER(%s) "
            "ORDER BY frequency DESC LIMIT 1",
            (phrase,),
        )
        row = cur.fetchone()
        if row:
            cur.close()
            conn.close()
            return {"target": row[0], "length": length, "freq": row[1]}
    cur.close()
    conn.close()
    return None


def add_phrase(source_phrase: str, target_phrase: str, frequency: int = 1) -> bool:
    """Add or update a phrase dictionary entry."""
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO phrase_dictionary (source_phrase, target_phrase, frequency) "
            "VALUES (%s, %s, %s) "
            "ON CONFLICT (source_phrase) "
            "DO UPDATE SET frequency = phrase_dictionary.frequency + EXCLUDED.frequency, "
            "target_phrase = EXCLUDED.target_phrase",
            (source_phrase, target_phrase, frequency),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def bulk_add_phrases(entries: list) -> int:
    """Add multiple phrase entries: [{source, target, freq}]."""
    conn = _conn()
    cur = conn.cursor()
    count = 0
    for e in entries:
        try:
            cur.execute(
                "INSERT INTO phrase_dictionary (source_phrase, target_phrase, frequency) "
                "VALUES (%s, %s, %s) "
                "ON CONFLICT (source_phrase) "
                "DO UPDATE SET frequency = phrase_dictionary.frequency + EXCLUDED.frequency, "
                "target_phrase = EXCLUDED.target_phrase",
                (e["source"], e["target"], e.get("freq", 1)),
            )
            count += 1
        except Exception:
            pass
    conn.commit()
    cur.close()
    conn.close()
    return count


def get_all_phrases(limit: int = 500) -> list:
    """Get all phrase entries ordered by frequency."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, source_phrase, target_phrase, frequency "
        "FROM phrase_dictionary "
        "ORDER BY frequency DESC LIMIT %s",
        (limit,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "source": r[1], "target": r[2], "freq": r[3]} for r in rows]


def phrase_count() -> int:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM phrase_dictionary")
    n = cur.fetchone()[0]
    cur.close()
    conn.close()
    return n


def add_entry(source_word: str, target_word: str, source_pos: str = "",
              target_pos: str = "", frequency: int = 1) -> bool:
    """Add or update a dictionary entry."""
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO translation_dictionary "
            "(source_word, target_word, source_pos, target_pos, frequency) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON CONFLICT (source_word, target_word, source_pos) "
            "DO UPDATE SET frequency = translation_dictionary.frequency + EXCLUDED.frequency, "
            "target_pos = EXCLUDED.target_pos",
            (source_word, target_word, source_pos, target_pos, frequency),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def bulk_add(entries: list) -> int:
    """Add multiple entries: [{source, target, source_pos, target_pos, freq}]."""
    conn = _conn()
    cur = conn.cursor()
    count = 0
    for e in entries:
        try:
            cur.execute(
                "INSERT INTO translation_dictionary "
                "(source_word, target_word, source_pos, target_pos, frequency) "
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (source_word, target_word, source_pos) "
                "DO UPDATE SET frequency = translation_dictionary.frequency + EXCLUDED.frequency, "
                "target_pos = EXCLUDED.target_pos",
                (e["source"], e["target"], e.get("source_pos", ""),
                 e.get("target_pos", ""), e.get("freq", 1)),
            )
            count += 1
        except Exception:
            pass
    conn.commit()
    cur.close()
    conn.close()
    return count


def search(prefix: str, limit: int = 50) -> list:
    """Search dictionary by source word prefix."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, source_word, target_word, source_pos, target_pos, frequency "
        "FROM translation_dictionary "
        "WHERE LOWER(source_word) LIKE LOWER(%s) "
        "ORDER BY frequency DESC LIMIT %s",
        (prefix + "%", limit),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "source": r[1], "target": r[2], "source_pos": r[3],
             "target_pos": r[4], "freq": r[5]} for r in rows]


def get_all(limit: int = 500, offset: int = 0) -> list:
    """Get all dictionary entries ordered by frequency."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, source_word, target_word, source_pos, target_pos, frequency "
        "FROM translation_dictionary "
        "ORDER BY frequency DESC LIMIT %s OFFSET %s",
        (limit, offset),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "source": r[1], "target": r[2], "source_pos": r[3],
             "target_pos": r[4], "freq": r[5]} for r in rows]


def count() -> int:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM translation_dictionary")
    n = cur.fetchone()[0]
    cur.close()
    conn.close()
    return n


def delete_entry_by_id(entry_id: int) -> bool:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM translation_dictionary WHERE id = %s", (entry_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return deleted


def delete_entry(source_word: str, target_word: str, source_pos: str) -> bool:
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM translation_dictionary "
        "WHERE LOWER(source_word) = LOWER(%s) AND LOWER(target_word) = LOWER(%s) "
        "AND LOWER(source_pos) = LOWER(%s)",
        (source_word, target_word, source_pos),
    )
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return deleted
