from src.services.geral_subjects.endereco import *
from src.infra.db.loader import *
from src.infra.db.connection import *
from src.infra.db.executor import *


def endereco_pipeline(
        df: pd.DataFrame,
        coluna: str
) -> pd.DataFrame:
    """
    Pipeline de normalização de endereço para uma coluna específica.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    normalizador = NormalizadorEndereco(df)

    normalizador.normalizar_coluna_endereco(coluna)

    return normalizador.df


def sql_bairros_unicos_alfa(
    df: pd.DataFrame,
    db_path: str,
    uf: str,
    *,
    sql_dir: str | Path = "sql/bairros",
    base_table: str = "staging__base",
) -> List[str]:
    """
    SQL-first pipeline.

    Entrada:
      - df com colunas: uf, bairro
      - db_path
      - uf (ex: "RJ")

    Etapas:
      1) carrega df -> SQLite em staging__base
      2) executa 01_drop_bairros_unicos.sql
      3) executa 02_create_bairros_unicos.sql (param :uf)
      4) executa 03_select_bairros_unicos_alfa.sql e retorna lista[str]
    """
    # Fail-fast
    if "uf" not in df.columns or "bairro" not in df.columns:
        raise ValueError("df precisa conter as colunas: 'uf' e 'bairro'.")

    uf_clean = str(uf).strip().upper()
    if not uf_clean:
        raise ValueError("uf não pode ser vazia.")

    sql_dir = Path(sql_dir)

    # 1) Load somente as colunas necessárias (contrato)
    df_to_sqlite(df[["uf", "bairro"]], db_path, base_table, mode="replace")

    # 2) Executa SQLs em ordem (SQL-first)
    exec_sql_file(db_path, sql_dir / "01_drop_bairros_unicos.sql")
    exec_sql_file(db_path, sql_dir / "02_create_bairros_unicos.sql", params={"uf": uf_clean})

    # 3) SELECT final -> lista
    select_sql = (sql_dir / "03_select_bairros_unicos_alfa.sql").read_text(encoding="utf-8")
    out = query_df(db_path, select_sql)

    # garante coluna esperada
    if "bairro" not in out.columns:
        raise RuntimeError("Query final não retornou a coluna 'bairro'.")

    return [str(x) for x in out["bairro"].tolist()]