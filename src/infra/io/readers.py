"""
Responsabilidade: ler arquivos e devolver dados em estrutura padrão (ex.: DataFrame).
"""
from pathlib import Path
import geopandas as gpd
import pandas as pd
import sqlite3
from typing import Optional


def read_gpkg_file(path: str | Path) -> pd.DataFrame:
    """
    Read a GeoPackage (.gpkg) file and return its contents as a pandas DataFrame.

    Args:
        path: File path as a string or pathlib.Path.

    Returns:
        DataFrame containing the GeoPackage data.

    Raises:
        ValueError: If the provided path is not a string or Path.
        IOError: If the file cannot be read.
    """
    if isinstance(path, Path):
        path = str(path)

    if not isinstance(path, str):
        raise ValueError("The file path must be a string or Path.")

    try:
        gdf = gpd.read_file(path)
    except Exception as e:
        raise IOError(f"Error reading gpkg file: {e}")

    return pd.DataFrame(gdf)


def query_sqlite_dataframe(
        db_path: str,
        table_name: Optional[str] = None,
        query: Optional[str] = None,
) -> pd.DataFrame:
    """
    Query a SQLite database and return the result as a pandas DataFrame.

    Args:
        db_path: Path to the SQLite database file (.db or .sqlite).
        table_name: Table name to query if `query` is not provided.
        query: Custom SQL query to execute.

    Returns:
        DataFrame containing the query results.

    Raises:
        ValueError: If `db_path` is not a string or if neither
            `table_name` nor `query` is provided.
        IOError: If the database query fails.
    """
    if not isinstance(db_path, str):
        raise ValueError("db_path must be a string.")

    if query is None and table_name is None:
        raise ValueError("Provide either `table_name` or `query`.")

    sql = query or f"SELECT * FROM {table_name}"

    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(sql, conn)
    except Exception as e:
        raise IOError(f"Error querying SQLite: {e}")

    return df


def read_client_csv_to_dataframe(
        path_csv: str | Path,
        sep: str = ",",
        encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Read a CSV file and return its contents as a pandas DataFrame.

    Responsibility:
        - File reading only.
        - No semantic validation.
        - No transformation logic.

    Args:
        path_csv: Path to the CSV file (string or Path).
        sep: Field separator used in the CSV file.
        encoding: File encoding.

    Returns:
        DataFrame containing the CSV data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a parsing error occurs while reading the file.
    """
    path = Path(path_csv)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_csv(
            path,
            sep=sep,
            encoding=encoding,
        )
    except pd.errors.ParserError as e:
        raise ValueError(f"CSV parsing error: {e}")

    return df


def read_client_xlsx_to_dataframe(
        path_xlsx: str | Path,
        sheet_name: str | int = 0,
) -> pd.DataFrame:
    """
    Read an XLSX file and return its contents as a pandas DataFrame.

    Responsibility:
        - File reading only.
        - No semantic validation.
        - No transformation logic.

    Args:
        path_xlsx: Path to the XLSX file (string or Path).
        sheet_name: Sheet name or index to read.

    Returns:
        DataFrame containing the Excel sheet data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If an error occurs while reading the XLSX file.
        ImportError: If the required Excel engine is not installed.
    """
    path = Path(path_xlsx)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            engine="openpyxl",
        )
    except ValueError as e:
        raise ValueError(f"Error reading XLSX file: {e}")
    except ImportError:
        raise ImportError(
            "openpyxl is not installed. Install it with: pip install openpyxl"
        )

    return df
