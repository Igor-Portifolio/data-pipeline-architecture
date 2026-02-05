# connection.py
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Optional, Sequence, Tuple, Union

SqlitePath = Union[str, Path]


# --- Defaults (you can override in connect_sqlite) ---------------------------

DEFAULT_PRAGMAS: Dict[str, Any] = {
    # Integrity / correctness
    "foreign_keys": 1,
    # Concurrency / performance (good defaults for most pipelines)
    "journal_mode": "WAL",      # allows concurrent readers
    "synchronous": "NORMAL",    # trade-off: fast + safe enough for most cases
    "busy_timeout": 5000,       # ms, helps avoid "database is locked"
    "temp_store": "MEMORY",
    "cache_size": -20000,       # negative = KiB; here ~20MB
}


@dataclass(frozen=True)
class ConnectionConfig:
    db_path: SqlitePath
    pragmas: Dict[str, Any] = None  # type: ignore[assignment]
    timeout: float = 30.0
    detect_types: int = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    isolation_level: Optional[str] = None  # None => autocommit mode (recommended with manual BEGIN)
    check_same_thread: bool = False  # useful if you run in worker threads


# --- Core helpers ------------------------------------------------------------

def connect_sqlite(
    db_path: SqlitePath,
    pragmas: Optional[Dict[str, Any]] = None,
    *,
    timeout: float = 30.0,
    detect_types: int = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    isolation_level: Optional[str] = None,
    check_same_thread: bool = False,
) -> sqlite3.Connection:
    """
    Open a SQLite connection and apply PRAGMAs.

    Design choice:
      - isolation_level=None => autocommit mode.
      - you control transactions explicitly with `transaction()` below.
    """
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        str(path),
        timeout=timeout,
        detect_types=detect_types,
        isolation_level=isolation_level,
        check_same_thread=check_same_thread,
    )
    conn.row_factory = sqlite3.Row

    apply_pragmas(conn, {**DEFAULT_PRAGMAS, **(pragmas or {})})
    return conn


def apply_pragmas(conn: sqlite3.Connection, pragmas: Dict[str, Any]) -> None:
    """
    Apply PRAGMAs safely.

    Notes:
      - Some PRAGMAs return a value (e.g., journal_mode). We don't need it here.
      - Values are interpolated carefully: identifiers are fixed ("PRAGMA <key>"),
        values are bound as parameters where possible.
    """
    cur = conn.cursor()
    try:
        for key, value in pragmas.items():
            _exec_pragma(cur, key, value)
    finally:
        cur.close()


def _exec_pragma(cur: sqlite3.Cursor, key: str, value: Any) -> None:
    # PRAGMA statements don't support binding for *all* shapes consistently,
    # but binding works for common scalar cases. For strings like WAL, it's fine.
    # We keep key strict to avoid injection via key.
    if not key.replace("_", "").isalnum():
        raise ValueError(f"Invalid PRAGMA key: {key!r}")

    if value is None:
        cur.execute(f"PRAGMA {key}")
        return

    # Some pragmas (journal_mode) often expect unquoted tokens, but binding works.
    cur.execute(f"PRAGMA {key} = ?", (value,))


# --- Transactions ------------------------------------------------------------

@contextmanager
def transaction(
    conn: sqlite3.Connection,
    *,
    mode: str = "IMMEDIATE",
) -> Iterator[sqlite3.Connection]:
    """
    Transaction context manager.

    mode:
      - "DEFERRED"  : lock only when needed
      - "IMMEDIATE" : reserves a write lock early (good for batch writes)
      - "EXCLUSIVE" : strongest lock (rarely needed)

    Behavior:
      - BEGIN <mode>
      - if ok -> COMMIT
      - if exception -> ROLLBACK and re-raise
    """
    mode_u = mode.strip().upper()
    if mode_u not in {"DEFERRED", "IMMEDIATE", "EXCLUSIVE"}:
        raise ValueError("mode must be one of: DEFERRED, IMMEDIATE, EXCLUSIVE")

    conn.execute(f"BEGIN {mode_u}")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


# --- Convenience execution helpers ------------------------------------------

def execute_many(
    conn: sqlite3.Connection,
    sql: str,
    rows: Iterable[Sequence[Any]],
) -> int:
    """
    executemany wrapper returning affected rowcount (best-effort; sqlite can return -1).
    """
    cur = conn.cursor()
    try:
        cur.executemany(sql, rows)
        return cur.rowcount
    finally:
        cur.close()


def execute_script(conn: sqlite3.Connection, script: str) -> None:
    """
    Execute a multi-statement SQL script (DDL/migrations).
    """
    conn.executescript(script)


def close_quietly(conn: Optional[sqlite3.Connection]) -> None:
    try:
        if conn is not None:
            conn.close()
    except Exception:
        # do not mask original errors in finally blocks
        pass
