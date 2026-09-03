import os
import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from typing import List, Dict, Optional, Tuple

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ir_system")
DB_USER = os.getenv("DB_USER", "ir_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ir_password")


def get_connection(apply_vector: bool = True):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    if apply_vector:
        register_vector(conn)
    return conn


def init_db():
    from migrate import run_migrations
    run_migrations()


def insert_document(title: str, content: str, embedding: List[float], summary: Optional[str] = None, file_path: Optional[str] = None) -> int:
    conn = get_connection()
    register_vector(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (title, content, embedding, summary, file_path) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (title, content, str(embedding), summary, file_path),
    )
    doc_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return doc_id


def search_documents(query_embedding: List[float], top_k: int = 10) -> List[Dict]:
    conn = get_connection()
    register_vector(conn)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, content,
               1 - (embedding <=> %s::vector) AS similarity,
               summary
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (str(query_embedding), str(query_embedding), top_k),
    )
    results = []
    for row in cur.fetchall():
        results.append({
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "similarity": float(row[3]),
            "summary": row[4],
        })
    cur.close()
    conn.close()
    return results


def get_all_documents() -> List[Dict]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, date_added, summary FROM documents ORDER BY id")
    results = []
    for row in cur.fetchall():
        results.append({
            "id": row[0],
            "title": row[1],
            "content": row[2][:500],
            "date_added": row[3].isoformat() if row[3] else None,
            "summary": row[4],
        })
    cur.close()
    conn.close()
    return results


def get_all_document_texts() -> List[str]:
    """Full (untruncated) content of every document — for vocab/IDF rebuilds."""
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT content FROM documents")
    texts = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return texts


def get_documents_without_summary() -> List[Dict]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM documents WHERE summary IS NULL OR summary = ''")
    docs = [{"id": row[0], "content": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return docs


def update_document_summary(doc_id: int, summary: str):
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("UPDATE documents SET summary = %s WHERE id = %s", (summary, doc_id))
    conn.commit()
    cur.close()
    conn.close()


def get_document_by_id(doc_id: int) -> Optional[Dict]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, date_added, summary FROM documents WHERE id = %s", (doc_id,))
    row = cur.fetchone()
    result = None
    if row:
        result = {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "date_added": row[3].isoformat() if row[3] else None,
            "summary": row[4],
        }
    cur.close()
    conn.close()
    return result


def delete_document(doc_id: int) -> bool:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return deleted


def log_search(query_text: str, query_embedding: List[float]):
    conn = get_connection()
    register_vector(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO search_logs (query_text, query_embedding) VALUES (%s, %s)",
        (query_text, str(query_embedding)),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_document_count() -> int:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM documents")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def save_vocabulary(vocab: Dict[str, int]):
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("DELETE FROM vocabulary")
    for word, idx in vocab.items():
        cur.execute(
            "INSERT INTO vocabulary (word, vector_index) VALUES (%s, %s)",
            (word, idx),
        )
    conn.commit()
    cur.close()
    conn.close()


def save_idf(idf: Dict[str, float]):
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("DELETE FROM idf_values")
    for word, val in idf.items():
        cur.execute(
            "INSERT INTO idf_values (word, idf_value) VALUES (%s, %s)",
            (word, val),
        )
    conn.commit()
    cur.close()
    conn.close()


def load_vocabulary() -> Optional[Dict[str, int]]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT word, vector_index FROM vocabulary")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return None
    return {row[0]: row[1] for row in rows}


def load_idf() -> Optional[Dict[str, float]]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT word, idf_value FROM idf_values")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return None
    return {row[0]: row[1] for row in rows}


def get_document_by_path(file_path: str) -> Optional[Dict]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, summary FROM documents WHERE file_path = %s", (file_path,))
    row = cur.fetchone()
    result = None
    if row:
        result = {"id": row[0], "title": row[1], "content": row[2], "summary": row[3]}
    cur.close()
    conn.close()
    return result


def upsert_document(title: str, content: str, embedding: List[float], summary: Optional[str], file_path: str) -> int:
    """Insert a document bound to file_path, or update it if it already exists."""
    conn = get_connection()
    register_vector(conn)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO documents (title, content, embedding, summary, file_path)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (file_path) WHERE file_path IS NOT NULL
        DO UPDATE SET title = EXCLUDED.title,
                      content = EXCLUDED.content,
                      embedding = EXCLUDED.embedding,
                      summary = EXCLUDED.summary,
                      date_added = CURRENT_TIMESTAMP
        RETURNING id
        """,
        (title, content, str(embedding), summary, file_path),
    )
    doc_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return doc_id


def delete_document_by_path(file_path: str) -> bool:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("DELETE FROM documents WHERE file_path = %s", (file_path,))
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return deleted


def register_watch_client(client_id: str, watched_dir: str):
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO watch_clients (client_id, watched_dir, registered_at, last_seen)
        VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT (client_id)
        DO UPDATE SET watched_dir = EXCLUDED.watched_dir, last_seen = CURRENT_TIMESTAMP
        """,
        (client_id, watched_dir),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_watch_clients() -> List[Dict]:
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute("SELECT client_id, watched_dir, registered_at, last_seen FROM watch_clients ORDER BY client_id")
    clients = [{
        "client_id": row[0],
        "watched_dir": row[1],
        "registered_at": row[2].isoformat() if row[2] else None,
        "last_seen": row[3].isoformat() if row[3] else None,
    } for row in cur.fetchall()]
    cur.close()
    conn.close()
    return clients


def log_watch_event(client_id: str, event_type: str, file_path: str, old_path: Optional[str] = None):
    conn = get_connection(apply_vector=False)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO watch_events (client_id, event_type, file_path, old_path) VALUES (%s, %s, %s, %s)",
        (client_id, event_type, file_path, old_path),
    )
    conn.commit()
    cur.close()
    conn.close()
