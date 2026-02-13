'''
Responsabilidade: resolver caminhos e padronizar onde ficam as coisas.

C:\projetos_solve\scripts_geral\src\infra\io\paths.py
'''

from __future__ import annotations
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
data_path = project_root / "data" / "raw"


def raw_data_file_path(filename: str) -> Path:
    """
    Retorna o Path absoluto para um arquivo dentro de data/raw.

    Regras:
      - filename deve conter extensão (ex: .csv, .xlsx)
      - filename não pode conter diretórios
      - apenas o nome completo do arquivo é permitido

    Exemplo:
        raw_file_path("clientes_2026.csv")
    """
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename deve ser uma string não vazia.")

    filename = filename.strip()

    # Não permitir caminho junto
    if Path(filename).name != filename:
        raise ValueError("Forneça apenas o nome do arquivo, sem diretórios.")

    # Obrigatório ter extensão
    if "." not in filename:
        raise ValueError("O nome do arquivo deve conter extensão (ex: .csv).")

    path = data_path / "client" / filename

    return path


staging_dir = data_path / "staging" / "clientes_limpos"
curated_dir = data_path / "curated" / "cliente_final"
logs_dir = data_path / "logs" / "nomes"
