import pandas as pd
from pathlib import Path


def exportar_fila_revisao_nomes(
    df_revisao: pd.DataFrame,
    path_saida: str,
    formato: str = "csv",
) -> str:
    """
    Exporta a fila de revisão de nomes para inspeção humana.

    Responsabilidade:
    - Apenas escrever o DataFrame em disco
    - Sobrescreve o arquivo se já existir
    """

    if formato.lower() != "csv":
        raise ValueError("Formato não suportado. Use apenas 'csv'.")

    path = Path(path_saida)

    df_revisao.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",  # importante para Excel
    )

    return str(path)
