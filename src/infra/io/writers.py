"""
Responsabilidade: escrever/exportar resultados.
"""

from pathlib import Path
import pandas as pd

def save_dataframe_to_csv(
    df: pd.DataFrame,
    path_csv: str | Path,
    sep: str = ",",
    encoding: str = "utf-8",
    index: bool = False,
) -> Path:
    """
    Save a pandas DataFrame to a CSV file.

    Responsibility:
        - File writing only.
        - No semantic validation.
        - No transformation logic.
        - Does not create directories.
        - Fails if the target directory does not exist.

    Args:
        df: DataFrame to be saved.
        path_csv: Destination file path (string or Path).
        sep: Field separator to use in the CSV file.
        encoding: File encoding.
        index: Whether to write row indices.

    Returns:
        Path to the saved CSV file.

    Raises:
        TypeError: If `df` is not a pandas DataFrame.
        ValueError: If the file extension is not ".csv".
        FileNotFoundError: If the target directory does not exist.
        IOError: If writing the file fails.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The provided object is not a pandas DataFrame.")

    path = Path(path_csv)

    if path.suffix.lower() != ".csv":
        raise ValueError("The file must have a .csv extension.")

    if not path.parent.exists():
        raise FileNotFoundError(
            f"The directory '{path.parent}' does not exist."
        )

    try:
        df.to_csv(
            path,
            sep=sep,
            encoding=encoding,
            index=index,
        )
    except Exception as e:
        raise IOError(f"Error saving CSV file: {e}")

    return path


