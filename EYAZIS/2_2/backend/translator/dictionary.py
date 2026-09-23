"""
Translation dictionary database operations.
Stores EN→FR word pairs and phrase pairs with POS tags and frequency.

PostgreSQL storage, LIST-partitioned by coarse POS group (pos_group) with
btree + GIN trigram indexes (migration 009).

Lookup chain: in-memory COMMON_WORDS -> exact SQL (partition-pruned)
              -> spaCy lemma retry -> fuzzy miss.
Search chain: prefix (text_pattern_ops) -> typo-tolerant similarity (pg_trgm).
"""
import os

import psycopg2

from translator.common_words import COMMON_WORDS
from translator import syntax_parser as _syntax_parser

# ── POS group mapping (must stay in sync with 009 migration CASE) ────

_FUNC_POS = frozenset({
    "IN", "TO", "CC", "DT", "EX", "WDT", "WP", "WP$", "WRB", "PRP", "PRP$",
    "MD", "POS", "RP", "UH", "PDT", "FW", "SYM", "CD",
    "DET", "PRE", "CON", "PRO", "NUM", "INT", "PONCT",
})


def pos_group(pos: str = "") -> str:
    """Fine Penn/WOLF POS tag -> coarse partition group."""
    if not pos:
        return "other"
    p = pos.upper()
    if p.startswith("NN") or p in ("NC", "N"):
        return "noun"
    if p.startswith("VB") or p in ("V", "VERB"):
        return "verb"
    if p.startswith("JJ") or p in ("ADJ", "A", "S"):
        return "adj"
    if p.startswith("RB") or p in ("ADV", "R"):
        return "adv"
    if p in _FUNC_POS:
        return "func"
    return "other"


def _conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "ir_system"),
        user=os.environ.get("DB_USER", "ir_user"),
        password=os.environ.get("DB_PASSWORD", "ir_password"),
    )


def _spacy_lemma(word: str) -> str:
    """English lemma via the spaCy pipeline already cached in syntax_parser
    (en_core_web_sm). Returns '' when the model is unavailable."""
    nlp = _syntax_parser._get_nlp("en")
    if nlp is None:
        return ""
    try:
        doc = nlp(word)
        for tok in doc:
            if tok.text.strip():
                return (tok.lemma_ or "").lower()
    except Exception:
        return ""
    return ""


def _sql_lookup(word_lower: str, pos: str = None) -> list:
    """Exact SQL lookup. When pos is given, add pos_group predicate so the
    planner prunes to a single partition, and fuzzy-match the fine tag
    (query 'NNS' matches stored 'NN'/'NNS'/'NNP')."""
    conn = _conn()
    cur = conn.cursor()
    try:
        if pos:
            cur.execute(
                "SELECT target_word, target_pos, frequency "
                "FROM translation_dictionary "
                "WHERE source_word = %s AND pos_group = %s "
                "AND (source_pos = %s OR source_pos LIKE %s) "
                "ORDER BY frequency DESC",
                (word_lower, pos_group(pos), pos.upper(), pos[:2].upper() + "%"),
            )
        else:
            cur.execute(
                "SELECT target_word, target_pos, frequency "
                "FROM translation_dictionary "
                "WHERE source_word = %s "
                "ORDER BY frequency DESC",
                (word_lower,),
            )
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return [{"target": r[0], "pos": r[1], "freq": r[2]} for r in rows]


def lookup(word: str, pos: str = None) -> list:
    """Find translations for a word, optionally filtered by POS.
    Chain: in-memory COMMON_WORDS -> exact SQL -> spaCy lemma retry."""
    lower = word.lower()

    # 1. Fast in-memory lookup
    if lower in COMMON_WORDS:
        fr, en_pos, fr_pos = COMMON_WORDS[lower]
        if pos is None or pos.upper() == en_pos.upper() or en_pos.startswith(pos[:2]):
            return [{"target": fr, "pos": fr_pos, "freq": 9999}]

    # 2. Exact SQL (partition-pruned when pos is given)
    rows = _sql_lookup(lower, pos)
    if rows:
        return rows

    # 3. Lemma retry: 'running' -> 'run' covers non-WordNet words too
    #    (translation_engine's WordNet lemma path runs before this on its side)
    lemma = _spacy_lemma(lower)
    if lemma and lemma != lower:
        return _sql_lookup(lemma, pos)
    return []


def lookup_phrase(words: tuple) -> dict:
    """Look up a multi-word phrase (tuple of lowercase words).
    Returns {target, length} or None."""
    conn = _conn()
    cur = conn.cursor()
    try:
        for length in range(len(words), 1, -1):
            phrase = " ".join(words[:length])
            cur.execute(
                "SELECT target_phrase, frequency "
                "FROM phrase_dictionary "
                "WHERE source_phrase = %s "
                "ORDER BY frequency DESC LIMIT 1",
                (phrase,),
            )
            row = cur.fetchone()
            if row:
                return {"target": row[0], "length": length, "freq": row[1]}
        return None
    finally:
        cur.close()
        conn.close()


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
            (source_phrase.lower(), target_phrase, frequency),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def bulk_add_phrases(entries: list, on_conflict: str = "update") -> int:
    """Add multiple phrase entries: [{source, target, freq}].
    on_conflict: 'update' accumulates frequency (bootstrap),
                 'skip' keeps the existing row untouched (seed)."""
    conn = _conn()
    cur = conn.cursor()
    count = 0
    skip_sql = (
        "INSERT INTO phrase_dictionary (source_phrase, target_phrase, frequency) "
        "VALUES (%s, %s, %s) ON CONFLICT (source_phrase) DO NOTHING"
    )
    update_sql = (
        "INSERT INTO phrase_dictionary (source_phrase, target_phrase, frequency) "
        "VALUES (%s, %s, %s) "
        "ON CONFLICT (source_phrase) "
        "DO UPDATE SET frequency = phrase_dictionary.frequency + EXCLUDED.frequency, "
        "target_phrase = EXCLUDED.target_phrase"
    )
    sql = update_sql if on_conflict == "update" else skip_sql
    for e in entries:
        try:
            cur.execute(sql, (e["source"].lower(), e["target"], e.get("freq", 1)))
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
    """Add or update a dictionary entry (partitioned insert)."""
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO translation_dictionary "
            "(source_word, target_word, source_pos, target_pos, pos_group, frequency) "
            "VALUES (%s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (source_word, target_word, source_pos, pos_group) "
            "DO UPDATE SET frequency = translation_dictionary.frequency + EXCLUDED.frequency, "
            "target_pos = EXCLUDED.target_pos",
            (source_word.lower(), target_word, (source_pos or "").upper(),
             target_pos, pos_group(source_pos), frequency),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def bulk_add(entries: list, on_conflict: str = "update") -> int:
    """Add multiple entries: [{source, target, source_pos, target_pos, freq}].
    on_conflict: 'update' accumulates frequency (bootstrap path),
                 'skip' keeps the existing row untouched (seed path)."""
    conn = _conn()
    cur = conn.cursor()
    count = 0
    skip_sql = (
        "INSERT INTO translation_dictionary "
        "(source_word, target_word, source_pos, target_pos, pos_group, frequency) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (source_word, target_word, source_pos, pos_group) DO NOTHING"
    )
    update_sql = (
        "INSERT INTO translation_dictionary "
        "(source_word, target_word, source_pos, target_pos, pos_group, frequency) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (source_word, target_word, source_pos, pos_group) "
        "DO UPDATE SET frequency = translation_dictionary.frequency + EXCLUDED.frequency, "
        "target_pos = EXCLUDED.target_pos"
    )
    sql = update_sql if on_conflict == "update" else skip_sql
    for e in entries:
        try:
            sp = (e.get("source_pos") or "").upper()
            cur.execute(sql, (
                e["source"].lower(), e["target"], sp,
                e.get("target_pos", ""), pos_group(sp), e.get("freq", 1),
            ))
            count += 1
        except Exception:
            pass
    conn.commit()
    cur.close()
    conn.close()
    return count


def _row_dict(r) -> dict:
    return {"id": r[0], "source": r[1], "target": r[2], "source_pos": r[3],
            "target_pos": r[4], "freq": r[5]}


def search(prefix: str, limit: int = 50) -> list:
    """Search dictionary by source word: exact prefix first
    (text_pattern_ops index), then typo-tolerant similarity (pg_trgm)
    to fill up to `limit` results."""
    p = (prefix or "").lower().strip()
    if not p:
        return get_all(limit=limit)
    conn = _conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, source_word, target_word, source_pos, target_pos, frequency "
            "FROM translation_dictionary "
            "WHERE source_word LIKE %s "
            "ORDER BY frequency DESC LIMIT %s",
            (p + "%", limit),
        )
        results = [_row_dict(r) for r in cur.fetchall()]

        if len(results) < limit:
            seen = {r["id"] for r in results}
            # '%' is the pg_trgm match operator -> must be escaped for psycopg2
            cur.execute(
                "SELECT id, source_word, target_word, source_pos, target_pos, frequency, "
                "similarity(source_word, %s) AS sim "
                "FROM translation_dictionary "
                "WHERE source_word %% %s "
                "ORDER BY sim DESC, frequency DESC LIMIT %s",
                (p, p, limit),
            )
            for r in cur.fetchall():
                if r[0] in seen:
                    continue
                results.append(_row_dict(r))
                seen.add(r[0])
                if len(results) >= limit:
                    break
        return results
    finally:
        cur.close()
        conn.close()


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
    return [_row_dict(r) for r in rows]


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
        "WHERE source_word = %s AND LOWER(target_word) = LOWER(%s) "
        "AND source_pos = %s AND pos_group = %s",
        (source_word.lower(), target_word, (source_pos or "").upper(),
         pos_group(source_pos)),
    )
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return deleted
