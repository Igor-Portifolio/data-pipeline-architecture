# connection.py
from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Optional, Sequence, Union

SqlitePath = Union[str, Path]

DEFAULT_PRAGMAS: Dict[str, Any] = {
    # Integrity / correctness
    "foreign_keys": 1,  # SQL nao ativa automaticamente
    # Concurrency / performance (good defaults for most pipelines)
    "synchronous": "NORMAL",  # trade-off: fast + safe enough for most cases | Nivel de segurança contra FE
    "busy_timeout": 5000,  # ms, helps avoid "database is locked" | 5 seg para func
    "temp_store": "MEMORY",  # tabelas temp vao para a rã
    "cache_size": -20000,  # negative = KiB; here ~20MB
}


# @dataclass(frozen=True)  # depois de criado nao poode ser alterado
# class ConnectionConfig:
#     db_path: SqlitePath
#     pragmas: Dict[str, Any] = None  # type: ignore[assignment]
#     timeout: float = 10
#     detect_types: int = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES # mantem os tipo de dados definidos
#     isolation_level: Optional[str] = None  # None => autocommit mode (recommended with manual BEGIN)
#     check_same_thread: bool = True


def connect_sqlite(
        db_path: SqlitePath,
        pragmas: Optional[Dict[str, Any]] = None,
        *,  # força tudo a ser passado como documento nomeado
        timeout: float = 10.0,
        detect_types: int = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        isolation_level: Optional[str] = None,
        check_same_thread: bool = True,
) -> sqlite3.Connection:
    """
    Create and configure a SQLite connection.

    This function:
        - Ensures the database directory exists.
        - Opens a SQLite connection with the provided configuration.
        - Sets `row_factory` to `sqlite3.Row`.
        - Applies default and user-provided PRAGMA settings.

    Transaction behavior:
        - `isolation_level=None` enables autocommit mode.
        - Explicit transaction control is expected via a separate
          transaction management utility.

    Args:
        db_path: Filesystem path to the SQLite database file.
        pragmas: Optional dictionary of PRAGMA settings to override
            or extend the defaults.
        timeout: Connection timeout in seconds.
        detect_types: SQLite type detection flags.
        isolation_level: SQLite isolation level. Use None for autocommit.
        check_same_thread: Whether the connection may be shared across threads.

    Returns:
        A configured `sqlite3.Connection` instance.
    """
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)  # cria diretorio caso nao exista

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
    Apply SQLite PRAGMA statements to an existing connection.

    This function iterates over a dictionary of PRAGMA key-value pairs
    and executes them sequentially on the provided connection.

    Security assumptions:
        - The `pragmas` dictionary is expected to originate from
          trusted internal configuration.
        - A minimal validation is performed on PRAGMA keys to prevent
          malformed or unsafe statements.

    Behavior:
        - If a value is None, executes `PRAGMA key`.
        - If a value is a string, wraps it in single quotes.
        - Otherwise, inserts the value directly into the statement.

    Args:
        conn: Active SQLite connection.
        pragmas: Dictionary mapping PRAGMA names to their desired values.

    Raises:
        ValueError: If a PRAGMA key contains invalid characters.
    """
    cur = conn.cursor()
    try:
        for key, value in pragmas.items():
            # validação simples da chave (evita coisas absurdas)
            key_clean = str(key).strip()
            if not key_clean.replace("_", "").isalnum():
                raise ValueError(f"Invalid PRAGMA key: {key!r}")

            if value is None:
                cur.execute(f"PRAGMA {key_clean}")
            else:
                # para string, coloca aspas simples
                if isinstance(value, str):
                    cur.execute(f"PRAGMA {key_clean} = '{value}'")
                else:
                    cur.execute(f"PRAGMA {key_clean} = {value}")
    finally:
        cur.close()


@contextmanager
def transaction(
        conn: sqlite3.Connection,
        *,
        mode: str = "IMMEDIATE",
) -> Iterator[sqlite3.Connection]:
    """
    Provide a transactional context manager for a SQLite connection.

    This context manager explicitly starts a transaction using
    `BEGIN <mode>` and ensures proper commit or rollback semantics.

    Supported modes:
        - "DEFERRED": Acquires locks only when required (default SQLite behavior).
        - "IMMEDIATE": Reserves a write lock at the beginning of the transaction.
        - "EXCLUSIVE": Acquires an exclusive lock for the duration of the transaction.

    Behavior:
        - Executes `BEGIN <mode>` upon entering the context.
        - Commits the transaction if the block completes successfully.
        - Rolls back the transaction if an exception occurs, then re-raises it.

    Args:
        conn: Active SQLite connection.
        mode: Transaction start mode. Must be one of
            {"DEFERRED", "IMMEDIATE", "EXCLUSIVE"}.

    Yields:
        The active SQLite connection within the transaction scope.

    Raises:
        ValueError: If an invalid transaction mode is provided.
        Any exception raised inside the context block is propagated
        after rollback.
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


def execute_many(
        conn: sqlite3.Connection,
        sql: str,
        rows: Iterable[Sequence[Any]],
) -> int:
    """
    Execute a parameterized SQL statement against multiple rows.

    This function wraps `cursor.executemany` and returns the number of
    affected rows. Note that SQLite may return -1 for `rowcount`
    depending on the statement type and driver behavior.

    Args:
        conn: Active SQLite connection.
        sql: Parameterized SQL statement to execute.
        rows: Iterable of parameter sequences to bind to the statement.

    Returns:
        Number of affected rows as reported by the cursor.
        May return -1 if the underlying driver does not provide
        a reliable row count.
    """

    cur = conn.cursor()
    try:
        cur.executemany(sql, rows)
        return cur.rowcount
    finally:
        cur.close()
