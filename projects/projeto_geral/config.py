from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from src.infra.io.paths import raw_data_file_path, logs_data_file_path, stagging_data_file_path, curated_data_file_path


class FileType(str, Enum):
    CSV = "csv"
    PARQUET = "parquet"
    XLSX = "xlsx"


@dataclass(frozen=True)
class ClientConfig:
    file_name: str
    file_type: FileType

    # colunas
    string_columns: list[str]
    email_column: str
    date_column: str
    name_column: str
    cpf_column: str
    phone_column: str


def build_paths(config: ClientConfig):
    stem = Path(config.file_name).stem
    extension = config.file_type.value

    input_file_path = raw_data_file_path(config.file_name)

    staging_file_name = f"{stem}_staging.{extension}"
    logs_file_name = f"{stem}_logs.csv"
    final_file_name = f"{stem}_RevA.{extension}"

    staging_file_path = stagging_data_file_path(staging_file_name)
    logs_file_path = logs_data_file_path(logs_file_name)
    curated_file_path = curated_data_file_path(final_file_name)

    return {
        "input": input_file_path,
        "staging": staging_file_path,
        "logs": logs_file_path,
        "curated": curated_file_path,
    }
