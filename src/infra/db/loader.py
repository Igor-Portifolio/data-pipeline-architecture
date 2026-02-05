# loader.py (simple)
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

from infra.connection import connect_sqlite, transaction, execute_many


@dataclass(frozen=True)
class SimpleLoadReport:
    table: str
    rows: int
    cols: List[str]
    mode: str


def df_to_sqlite(
    df: "pd.DataFrame",
    db_path: str,
    table: str,
    *,
    mode: str = "replace",   # "replace" | "append"
    chunksize: int = 50_000,
    pragmas: Optional[Dict[str, Any]] = None,
) -> SimpleLoadReport:
    """
    Minimal pipeline:
      - open connection
      - (replace|append) table
      - create table from df columns
      - bulk insert df
    """
    _require_pandas()
    if mode not in {"replace", "append"}:
        raise ValueError("mode must be 'replace' or 'append'")

    table = _safe_name(table)
    df2 = _prepare_df(df)
    cols = [ _safe_name(c) for c in df2.columns.tolist() ]

    # rename columns if needed
    if cols != df2.columns.tolist():
        df2 = df2.rename(columns=dict(zip(df2.columns.tolist(), cols)))

    conn = connect_sqlite(db_path, pragmas=pragmas)
    try:
        with transaction(conn, mode="IMMEDIATE"):
            if mode == "replace":
                conn.execute(f'DROP TABLE IF EXISTS "{table}"')

            ensure_table_from_df(conn, table, df2)
            insert_df(conn, table, df2, chunksize=chunksize)

        return SimpleLoadReport(table=table, rows=int(df2.shape[0]), cols=cols, mode=mode)
    finally:
        conn.close()


def ensure_table_from_df(conn: sqlite3.Connection, table: str, df: "pd.DataFrame") -> None:
    """
    Create table if not exists, based on df columns.
    Simple type inference:
      - int -> INTEGER
      - float -> REAL
      - bool -> INTEGER
      - datetime -> TEXT
      - everything else -> TEXT
    """
    _require_pandas()
    cols = df.columns.tolist()

    dtype_map = {}
    for c in cols:
        dtype_map[c] = _infer_sqlite_type(df[c])

    col_defs = [f'"{c}" {dtype_map[c]}' for c in cols]
    ddl = f'CREATE TABLE IF NOT EXISTS "{table}" (\n  ' + ",\n  ".join(col_defs) + "\n);"
    conn.execute(ddl)


def insert_df(
    conn: sqlite3.Connection,
    table: str,
    df: "pd.DataFrame",
    *,
    chunksize: int = 50_000,
) -> int:
    """
    Bulk insert DataFrame (assumes table exists).
    Caller controls transaction scope.
    """
    _require_pandas()

    if df.shape[0] == 0:
        return 0

    cols = df.columns.tolist()
    placeholders = ", ".join(["?"] * len(cols))
    col_sql = ", ".join(f'"{c}"' for c in cols)
    sql = f'INSERT INTO "{table}" ({col_sql}) VALUES ({placeholders})'

    total = 0
    n = int(df.shape[0])
    chunksize = max(1, int(chunksize))

    for start in range(0, n, chunksize):
        end = min(start + chunksize, n)
        chunk = df.iloc[start:end]
        rows = _chunk_to_rows(chunk)
        execute_many(conn, sql, rows)
        total += len(rows)

    return total


# ----------------- internal helpers -----------------

def _require_pandas() -> None:
    if pd is None:
        raise RuntimeError("pandas is required for loader.py (install pandas).")


def _prepare_df(df: "pd.DataFrame") -> "pd.DataFrame":
    df2 = df.copy()
    # SQLite wants Python None (not NaN)
    df2 = df2.where(pd.notnull(df2), None)
    return df2


def _infer_sqlite_type(s: "pd.Series") -> str:
    dt = str(s.dtype)

    if dt.startswith("int") or dt.startswith("Int"):
        return "INTEGER"
    if dt.startswith("float"):
        return "REAL"
    if dt == "bool" or dt == "boolean":
        return "INTEGER"
    if "datetime64" in dt:
        return "TEXT"
    return "TEXT"


def _safe_name(name: Any) -> str:
    name = str(name).strip()
    if not name:
        raise ValueError("Empty table/column name")

    # replace invalid chars with underscore
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", name).strip("_")
    if not cleaned:
        raise ValueError(f"Invalid name: {name!r}")

    # avoid leading digit
    if cleaned[0].isdigit():
        cleaned = f"c_{cleaned}"

    return cleaned


def _chunk_to_rows(chunk: "pd.DataFrame") -> List[Tuple[Any, ...]]:
    values = chunk.to_numpy(dtype=object)
    return [tuple(r) for r in values]
