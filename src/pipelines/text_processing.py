from src.services.text_normalization_service import TextNormalizationService
from src.infra.io.writers import save_dataframe_to_csv
from pathlib import Path
from src.review.name_review import apply_name_review
from src.review.name_review import collect_suspicious_name_cases
import pandas as pd


def text_normalization_and_validation(
        df: pd.DataFrame,
        columns_strings: str | list[str],
        column_email: str | list[str] | None = None,
        column_name: str | list[str] | None = None,
        column_cpf: str | None = None,
        column_tel: str | None = None,
) -> pd.DataFrame:
    """
    Run a basic text normalization pipeline over selected DataFrame columns.

    Steps:
        - Normalize text columns (uppercase + remove diacritics).
        - Optionally move misplaced emails from name column to email column.
        - Optionally normalize and validate email column(s).
        - Optionally clean proper names column(s).
        - Optionally normalize CPF column.
        - Optionally normalize telephone column.

    Args:
        df: Input pandas DataFrame.
        columns_strings: Column name or list of column names to normalize as text.
        column_email: Email column name or list of column names.
        column_name: Name column name or list of column names.
        column_cpf: CPF column name.
        column_tel: Telephone column name.

    Returns:
        A DataFrame with text-related transformations applied.

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
        ValueError: If provided column parameters are not of the expected type.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    cleaner = TextNormalizationService(df)
    cleaner.normalize_text(
        columns=columns_strings,
        upper=True,
        remove_diacritics=True,
    )

    if column_email is not None and column_name is not None:
        if not isinstance(column_name, (str, list)):
            raise ValueError(
                "column_name must be a str or list[str] when provided."
            )
        if not isinstance(column_email, (str, list)):
            raise ValueError(
                "column_email must be a str or list[str] when provided."
            )
        cleaner.move_email_from_name_column(
            column_email=column_email,
            column_name=column_name,
        )

    if column_email is not None:
        if not isinstance(column_email, (str, list)):
            raise ValueError(
                "column_email must be a str or list[str] when provided."
            )
        cleaner.normalize_text(
            columns=column_email,
            lower=True,
        )
        cleaner.validate_email_column(
            column=column_email,
        )

    if column_name is not None:
        if not isinstance(column_name, (str, list)):
            raise ValueError(
                "column_name must be a str or list[str] when provided."
            )
        cleaner.clean_proper_names_column(
            column=column_name,
        )

    if column_cpf is not None:
        if not isinstance(column_cpf, str):
            raise ValueError(
                "column_cpf must be a non-empty string when provided."
            )
        cleaner.normalize_cpf_column(
            column=column_cpf,
        )

    if column_tel is not None:
        if not isinstance(column_tel, str):
            raise ValueError(
                "column_tel must be a non-empty string when provided."
            )
        cleaner.normalize_phone_column(
            column=column_tel,
        )

    return cleaner.df


# def text_names_part_one_pipeline(
#         df: pd.DataFrame,
#         coluna_nome: str
# ) -> pd.DataFrame:
#     if not isinstance(df, pd.DataFrame):
#         raise TypeError("Entrada deve ser um pandas DataFrame")
#
#     cleaner = Standard_text(df)
#
#     cleaner.remover_valores_sem_letras(coluna_nome)
#     cleaner.limpar_nomes_proprios(coluna_nome)
#
#     return cleaner.df


def proper_name_review_queue_export(
        df: pd.DataFrame,
        column_name: str,
        logs_file_dir: str | Path,
) -> pd.DataFrame:
    """
    Collect suspicious proper-name cases and export a review queue to CSV.

    This pipeline:
        1) Collects suspicious name cases for human inspection.
        2) Exports the resulting review queue to a CSV file.

    Args:
        df: Input pandas DataFrame.
        column_name: Name of the column containing proper names to inspect.
        logs_file_dir: Output directory or file path used to store the CSV export.

    Returns:
        The original DataFrame (unchanged).

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
        KeyError: If `coluna_nome` does not exist in the DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' not found in DataFrame.")

    df_revisao = collect_suspicious_name_cases(
        df=df,
        column=column_name,
    )

    save_dataframe_to_csv(df_revisao, logs_file_dir)

    return df


def proper_name_apply_review_log(
        df: pd.DataFrame,
        column_name: str,
        logs_file_dir: str | Path,
) -> pd.DataFrame:
    """
    Apply approved proper-name reviews from a CSV log to the original DataFrame.

    This pipeline:
        1) Reads a review queue CSV file (if it exists).
        2) Applies approved revisions to the original DataFrame.

    If the log file does not exist or contains no rows, the input DataFrame is
    returned unchanged.

    Args:
        df: Input pandas DataFrame.
        column_name: Name of the column containing proper names to be updated.
        logs_file_dir: Path to the CSV file containing approved reviews.

    Returns:
        A DataFrame with approved name revisions applied, or the original DataFrame
        if no revisions are available.

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
        KeyError: If `coluna_nome` does not exist in the DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' not found in DataFrame.")

    path = Path(logs_file_dir)

    if not path.exists():
        return df

    df_logs = pd.read_csv(path, encoding="utf-8-sig")

    if df_logs.empty:
        return df

    df_final = apply_name_review(
        df_original=df,
        df_logs=df_logs,
        column_name=column_name,
    )

    return df_final
