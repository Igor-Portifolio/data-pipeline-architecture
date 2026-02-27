from pathlib import Path
import pandas as pd


def export_review_queue(
    df_revisao: pd.DataFrame,
    path_saida: str,
    formato: str = "csv",
) -> str:
    """
    Export a review queue DataFrame to disk for human inspection.

    Args:
        df_revisao: DataFrame to be exported.
        path_saida: Output file path.
        formato: Export format. Currently only "csv" is supported.

    Returns:
        The output file path as a string.

    Raises:
        ValueError: If the provided format is not supported.
    """

    if formato.lower() != "csv":
        raise ValueError("Unsupported format. Only 'csv' is allowed.")

    path = Path(path_saida)

    df_revisao.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
    )

    return str(path)