from pathlib import Path
import geopandas as gpd
import pandas as pd
import sqlite3
from typing import Optional


def ler_arquivo_gpkg(path) -> pd.DataFrame:
    """
    Lê um arquivo GeoPackage (.gpkg) e retorna um DataFrame.
    Aceita str ou pathlib.Path.
    """

    if isinstance(path, Path):
        path = str(path)

    if not isinstance(path, str):
        raise ValueError("O caminho do arquivo deve ser str ou Path.")

    try:
        gdf = gpd.read_file(path)
    except Exception as e:
        raise IOError(f"Erro ao ler arquivo gpkg: {e}")

    return pd.DataFrame(gdf)


def consultar_df_sqlite(
    db_path: str,
    table_name: Optional[str] = None,
    query: Optional[str] = None
) -> pd.DataFrame:
    """
    Consulta dados em um banco SQLite e retorna um DataFrame.

    Parâmetros:
        db_path: caminho do arquivo .db / .sqlite
        table_name: nome da tabela (usado se query não for fornecida)
        query: SQL customizado (opcional)

    Retorno:
        pd.DataFrame com os dados consultados
    """

    if not isinstance(db_path, str):
        raise ValueError("db_path deve ser uma string.")

    if query is None and table_name is None:
        raise ValueError("Informe table_name ou query.")

    sql = query or f"SELECT * FROM {table_name}"

    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql(sql, conn)
    except Exception as e:
        raise IOError(f"Erro ao consultar SQLite: {e}")

    return df

