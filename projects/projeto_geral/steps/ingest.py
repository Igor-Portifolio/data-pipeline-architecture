from __future__ import annotations

from pathlib import Path

from projects.projeto_geral.context import ProjectContext, StepState
from src.infra.io.readers import ler_csv_clinte_para_df


def run(ctx: ProjectContext, state: StepState) -> StepState:
    """
    Step de ingestão.

    Responsável por:
    - Ler o arquivo bruto do cliente
    - Validar existência do arquivo
    - Carregar DataFrame inicial no state
    """

    input_path: Path = ctx.paths["input"]

    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")

    print(f"[INGEST] Lendo arquivo: {input_path}")

    # Atualmente suportando CSV
    # Futuramente você pode expandir baseado em ctx.config.file_type
    df = ler_csv_clinte_para_df(input_path)

    if df.empty:
        print("[INGEST] Aviso: DataFrame carregado está vazio.")

    state.df = df

    print(f"[INGEST] Linhas carregadas: {len(df)}")

    return state
