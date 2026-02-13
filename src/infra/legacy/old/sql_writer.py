import pandas as pd
import sqlite3


def salvar_df_sqlite(
    df: pd.DataFrame,
    db_path: str,
    table_name: str,
    modo: str = "append"
) -> None:
    """
    Persiste um DataFrame em uma tabela SQLite.

    Parâmetros:
        df: DataFrame a ser salvo
        db_path: caminho do arquivo .sqlite / .db
        table_name: nome da tabela de destino
        modo: 'append' ou 'replace'
    """

    if modo not in {"append", "replace"}:
        raise ValueError("modo deve ser 'append' ou 'replace'.")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df deve ser um pandas DataFrame.")

    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists=modo,
                index=False
            )
    except Exception as e:
        raise IOError(f"Erro ao salvar DataFrame no SQLite: {e}")
