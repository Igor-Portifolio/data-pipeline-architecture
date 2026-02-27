"""
Responsibility: resolve paths and standardize where components and resources are located.
"""

from __future__ import annotations
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
data_path = project_root / "data" / "raw"
staging_dir = project_root / "data" / "staging" / "clientes_limpos"
curated_dir = project_root / "data" / "curated" / "cliente_final"
logs_dir = project_root / "data" / "logs" / "nomes"


def raw_data_file_path(filename: str) -> Path:
    """
    Return the absolute Path to a file inside the data/raw directory.

    Rules:
        - `filename` must include a file extension (e.g., ".csv", ".xlsx").
        - `filename` must not contain directory components.
        - Only the complete file name is allowed.

    Example:
        raw_data_file_path("clientes_2026.csv")
    """
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string.")

    filename = filename.strip()

    if Path(filename).name != filename:
        raise ValueError("Provide only the file name, without directories.")

    if "." not in filename:
        raise ValueError("The file name must contain an extension (e.g., .csv).")

    path = data_path / "client" / filename

    return path


def staging_data_file_path(filename: str) -> Path:
    """
    Return the absolute Path to a file inside the data/raw directory.

    Rules:
        - `filename` must include a file extension (e.g., ".csv", ".xlsx").
        - `filename` must not contain directory components.
        - Only the complete file name is allowed.

    Args:
        filename: Name of the file to resolve.

    Returns:
        Absolute Path pointing to the file inside the data/raw directory.

    Raises:
        ValueError: If the filename is empty, contains directories,
        or does not include a file extension.
    """
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string.")

    filename = filename.strip()

    if Path(filename).name != filename:
        raise ValueError("Provide only the file name, without directories.")

    if "." not in filename:
        raise ValueError("The file name must contain an extension (e.g., .csv).")

    path = staging_dir / filename

    return path


def curated_data_file_path(filename: str) -> Path:
    """
    Return the absolute Path to a file inside the curated directory.

    Rules:
        - `filename` must include a file extension (e.g., ".csv", ".xlsx").
        - `filename` must not contain directory components.
        - Only the complete file name is allowed.

    Args:
        filename: Name of the file to resolve.

    Returns:
        Absolute Path pointing to the file inside the curated directory.

    Raises:
        ValueError: If the filename is empty, contains directories,
        or does not include a file extension.
    """
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string.")

    filename = filename.strip()

    if Path(filename).name != filename:
        raise ValueError("Provide only the file name, without directories.")

    if "." not in filename:
        raise ValueError("The file name must contain an extension (e.g., .csv).")

    path = curated_dir / filename

    return path


def logs_data_file_path(filename: str) -> Path:
    """
    Return the absolute Path to a file inside the logs directory.

    Rules:
        - `filename` must include a file extension (e.g., ".csv", ".xlsx").
        - `filename` must not contain directory components.
        - Only the complete file name is allowed.

    Args:
        filename: Name of the file to resolve.

    Returns:
        Absolute Path pointing to the file inside the logs directory.

    Raises:
        ValueError: If the filename is empty, contains directories,
        or does not include a file extension.
    """
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string.")

    filename = filename.strip()

    if Path(filename).name != filename:
        raise ValueError("Provide only the file name, without directories.")

    if "." not in filename:
        raise ValueError("The file name must contain an extension (e.g., .csv).")

    path = logs_dir / filename

    return path
