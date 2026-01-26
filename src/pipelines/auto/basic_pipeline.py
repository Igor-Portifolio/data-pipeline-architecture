from src.services.basic import *


def basic_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline básico de limpeza genérica de dados.
    Ordem:
    1. Normalização de nulos
    2. Remoção de duplicatas exatas
    3. Trim de whitespace
    4. Coerção de tipos
    5. Normalização de pontuação
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Basic_clean(df)

    (
        cleaner
        .normalize_nulls()
        .drop_exact_duplicates()
        .trim_whitespace()
        .coerce_types()
        .normalizar_pontuacao()
    )

    return cleaner.df
