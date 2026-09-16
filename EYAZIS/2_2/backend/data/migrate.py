import os
import glob
import psycopg2
from typing import List

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ir_system")
DB_USER = os.getenv("DB_USER", "ir_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ir_password")

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def get_applied_migrations(conn) -> set:
    cur = conn.cursor()
    try:
        cur.execute("SELECT migration_name FROM schema_migrations ORDER BY id")
        return {row[0] for row in cur.fetchall()}
    except psycopg2.errors.UndefinedTable:
        conn.rollback()
        return set()
    finally:
        cur.close()


def get_migration_files() -> List[str]:
    pattern = os.path.join(MIGRATIONS_DIR, "*.sql")
    files = glob.glob(pattern)
    files.sort()
    return files


def extract_migration_name(filepath: str) -> str:
    basename = os.path.basename(filepath)
    name, _ = os.path.splitext(basename)
    return name


def run_migrations():
    conn = get_connection()
    try:
        applied = get_applied_migrations(conn)
        migration_files = get_migration_files()

        if not migration_files:
            print("No migration files found.")
            return

        pending = []
        for f in migration_files:
            name = extract_migration_name(f)
            if name not in applied:
                pending.append((name, f))

        if not pending:
            print("All migrations already applied.")
            return

        for name, filepath in pending:
            print(f"Applying migration: {name}")
            with open(filepath, "r") as fh:
                sql = fh.read()

            cur = conn.cursor()
            try:
                cur.execute(sql)
                conn.commit()
                print(f"  OK: {name}")
            except Exception as e:
                conn.rollback()
                print(f"  FAILED: {name} - {e}")
                raise
            finally:
                cur.close()

        print(f"Applied {len(pending)} migration(s).")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migrations()
