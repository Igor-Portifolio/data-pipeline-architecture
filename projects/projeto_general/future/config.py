from dataclasses import dataclass
from enum import Enum
from typing import Optional

class FileType(str, Enum):
    CSV = "csv"
    PARQUET = "parquet"
    XLSX = "xlsx"


@dataclass(frozen=True)
class ClientConfig:
    file_name: str
    file_type: FileType

    string_columns: list[str]

    email_column: Optional[str] = None
    date_column: Optional[str] = None
    name_column: Optional[str] = None
    cpf_column: Optional[str] = None
    phone_column: Optional[str] = None



config = ClientConfig(
        file_name="projeto_teste.csv",
        file_type=FileType.CSV,
        string_columns=["nome", "status"],
        email_column="email",
        cpf_column=None,  # exemplo de coluna ausente
    )




