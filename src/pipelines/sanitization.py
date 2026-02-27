from src.services.dataframe_cleaning_service import *


def full_sanitization(df: pd.DataFrame, column_date: str | None = None) -> pd.DataFrame:
    """
    Run a full structural sanitization pipeline on a DataFrame.

    This pipeline performs the following steps in order:
        1. Normalize null-like values.
        2. Remove exact duplicate rows.
        3. Trim whitespace from all values.
        4. Coerce scalar values to inferred types (int, float, datetime).
        5. Optionally format a date column to 'dd/mm/yyyy'.

    Args:
        df: Input pandas DataFrame to be sanitized.
        column_date: Optional column name to format as 'dd/mm/yyyy'.
            Must be a non-empty string if provided.

    Returns:
        A sanitized pandas DataFrame.

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
        ValueError: If `coluna_data` is provided but is not a valid non-empty string.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = DataFrameSanitizationService(df)
    cleaner.normalize_nulls()
    cleaner.drop_exact_duplicates()
    cleaner.trim_whitespace()
    cleaner.coerce_types()

    if column_date is not None:
        if not isinstance(column_date, str) or not column_date.strip():
            raise ValueError("coluna_data deve ser uma string não vazia quando fornecida.")
        cleaner.format_date_column_ddmmyyyy(column_date.strip())

    # cleaner.normalizar_pontuacao()
    return cleaner.df


def final_null_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run a final null normalization pass on a DataFrame.

    This pipeline performs a single structural step:
        - Normalize null-like values across all columns.

    It is intended to be used as a post-processing step
    after additional transformations that may reintroduce
    null-like tokens.

    Args:
        df: Input pandas DataFrame to normalize.

    Returns:
        A DataFrame with null-like values standardized to pd.NA.

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = DataFrameSanitizationService(df)
    cleaner.normalize_nulls()

    return cleaner.df
