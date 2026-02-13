# connection.py
from __future__ import annotations
import sqlite3
from contextlib import contextmanager  # controle automatico de abrir e fechar a função
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Optional, Sequence, Tuple, Union

SqlitePath = Union[str, Path]  # aceita tanto string como path no caminho do banco

# --- Defaults (you can override in connect_sqlite) ---------------------------

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


# --- Core helpers ------------------------------------------------------------

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
    Open a SQLite connection and apply PRAGMAs.

    Design choice:
      - isolation_level=None => autocommit mode.
      - you control transactions explicitly with `transaction()` below.
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
    Apply PRAGMAs in a simplified way.
    Assumes pragmas come from trusted internal configuration.
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






