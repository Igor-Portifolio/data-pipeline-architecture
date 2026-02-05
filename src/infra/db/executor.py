# executor.py
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple, Union

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

from infra.connection import connect_sqlite, transaction


SqlParams = Union[Sequence[Any], Mapping[str, Any]]
SqlitePath = Union[str, Path]


@dataclass(frozen=True)
class MaterializeReport:
    name: str
    kind: str  # "table" | "view"
    mode: str  # "replace" | "fail"
    rowcount: Optional[int]


# ----------------------------
# Public API
# ----------------------------

def exec_sql_file(
    db_path: SqlitePath,
    sql_path: SqlitePath,
    *,
    params: Optional[SqlParams] = None,
    pragmas: Optional[Dict[str, Any]] = None,
    transactional: bool = True,
) -> None:
    """
    Execute a .sql file (can contain multiple statements).

    Use this for:
      - schema (DDL)
      - seeds
      - migrations
      - any multi-statement script

    Notes:
      - If `params` is provided, the file must contain ONE statement (not multiple),
        because sqlite executescript does not accept parameters.
    """
    script = Path(sql_path).read_text(encoding="utf-8")

    conn = connect_sqlite(db_path, pragmas=pragmas)
    try:
        if params is None:
            if transactional:
                with transaction(conn, mode="IMMEDIATE"):
                    conn.executescript(script)
            else:
                conn.executescript(script)
        else:
            # Parameterized execution => single statement only
            if transactional:
                with transaction(conn, mode="IMMEDIATE"):
                    conn.execute(script, params)
            else:
                conn.execute(script, params)
    finally:
        conn.close()


def query_df(
    db_path: SqlitePath,
    sql: str,
    *,
    params: Optional[SqlParams] = None,
    pragmas: Optional[Dict[str, Any]] = None,
) -> "pd.DataFrame":
    """
    Run a SELECT query and return a pandas DataFrame.

    Requires pandas.
    """
    _require_pandas()

    conn = connect_sqlite(db_path, pragmas=pragmas)
    try:
        cur = conn.execute(sql, params or ())
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return pd.DataFrame(rows, columns=cols)
    finally:
        conn.close()


def materialize_table(
    db_path: SqlitePath,
    name: str,
    select_sql: str,
    *,
    params: Optional[SqlParams] = None,
    mode: str = "replace",  # "replace" | "fail"
    pragmas: Optional[Dict[str, Any]] = None,
    add_indexes: Optional[Sequence[Sequence[str]]] = None,
) -> MaterializeReport:
    """
    Materialize a TABLE from a SELECT query.

    Implementation uses:
      - CREATE TABLE AS SELECT ...  (CTAS)
    """
    name = _safe_identifier(name)
    _validate_mode(mode)

    conn = connect_sqlite(db_path, pragmas=pragmas)
    try:
        with transaction(conn, mode="IMMEDIATE"):
            if mode == "replace":
                conn.execute(f'DROP TABLE IF EXISTS "{name}"')
            elif mode == "fail" and _object_exists(conn, name):
                raise RuntimeError(f"Object already exists: {name}")

            # CTAS
            if params is None:
                conn.execute(f'CREATE TABLE "{name}" AS {select_sql}')
            else:
                conn.execute(f'CREATE TABLE "{name}" AS {select_sql}', params)

            # optional indexes
            if add_indexes:
                for cols in add_indexes:
                    _create_index(conn, table=name, cols=list(cols))

            # rowcount is not reliable in sqlite for CTAS; fetch count
            rc = _count_rows(conn, name)
            return MaterializeReport(name=name, kind="table", mode=mode, rowcount=rc)
    finally:
        conn.close()


def materialize_view(
    db_path: SqlitePath,
    name: str,
    select_sql: str,
    *,
    mode: str = "replace",  # "replace" | "fail"
    pragmas: Optional[Dict[str, Any]] = None,
) -> MaterializeReport:
    """
    Materialize a VIEW from a SELECT query.

    Notes:
      - SQLite doesn't support parameters in CREATE VIEW the way you expect.
        Pass a fully rendered select_sql (no params).
    """
    name = _safe_identifier(name)
    _validate_mode(mode)

    conn = connect_sqlite(db_path, pragmas=pragmas)
    try:
        with transaction(conn, mode="IMMEDIATE"):
            if mode == "replace":
                conn.execute(f'DROP VIEW IF EXISTS "{name}"')
            elif mode == "fail" and _object_exists(conn, name):
                raise RuntimeError(f"Object already exists: {name}")

            conn.execute(f'CREATE VIEW "{name}" AS {select_sql}')
            return MaterializeReport(name=name, kind="view", mode=mode, rowcount=None)
    finally:
        conn.close()


def exec_sql(
    db_path: SqlitePath,
    sql: str,
    *,
    params: Optional[SqlParams] = None,
    pragmas: Optional[Dict[str, Any]] = None,
    transactional: bool = True,
) -> None:
    """
    Execute a single SQL statement (DDL/DML). No return.
    """
    conn = connect_sqlite(db_path, pragmas=pragmas)
    try:
        if transactional:
            with transaction(conn, mode="IMMEDIATE"):
                conn.execute(sql, params or ())
        else:
            conn.execute(sql, params or ())
    finally:
        conn.close()


# ----------------------------
# Internals
# ----------------------------

def _require_pandas() -> None:
    if pd is None:
        raise RuntimeError("pandas is required for query_df() (install pandas).")


def _validate_mode(mode: str) -> None:
    if mode not in {"replace", "fail"}:
        raise ValueError("mode must be 'replace' or 'fail'")


def _safe_identifier(name: str) -> str:
    name = str(name).strip()
    if not name:
        raise ValueError("Empty identifier")
    # conservative: allow letters, numbers, underscore only
    import re
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", name).strip("_")
    if not cleaned:
        raise ValueError(f"Invalid identifier: {name!r}")
    if cleaned[0].isdigit():
        cleaned = f"obj_{cleaned}"
    return cleaned


def _object_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE name=? AND type IN ('table','view') LIMIT 1",
        (name,),
    ).fetchone()
    return row is not None


def _count_rows(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f'SELECT COUNT(1) AS n FROM "{table}"').fetchone()
    return int(row["n"]) if row and "n" in row.keys() else int(row[0])


def _create_index(conn: sqlite3.Connection, table: str, cols: list[str]) -> None:
    if not cols:
        return
    cols = [_safe_identifier(c) for c in cols]
    idx_name = f"idx__{table}__" + "__".join(cols)
    cols_sql = ", ".join(f'"{c}"' for c in cols)
    conn.execute(f'CREATE INDEX IF NOT EXISTS "{idx_name}" ON "{table}" ({cols_sql});')
