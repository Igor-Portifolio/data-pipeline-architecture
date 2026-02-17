from src.services.geral_subjects.basic import *


def basic_pipeline_1st(df: pd.DataFrame, coluna_data: str | None = None) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Basic_clean(df)
    cleaner.normalize_nulls()
    cleaner.drop_exact_duplicates()
    cleaner.trim_whitespace()
    cleaner.coerce_types()

    if coluna_data is not None:
        if not isinstance(coluna_data, str) or not coluna_data.strip():
            raise ValueError("coluna_data deve ser uma string não vazia quando fornecida.")
        cleaner.formatar_coluna_data_ddmmaaaa(coluna_data.strip())

    # cleaner.normalizar_pontuacao()
    return cleaner.df


def basic_pipeline_2st(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Basic_clean(df)
    cleaner.normalize_nulls()

    return cleaner.df
