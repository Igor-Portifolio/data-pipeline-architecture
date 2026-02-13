'''
Responsabilidade: escrever/exportar resultados.
'''

from pathlib import Path
import pandas as pd


def salvar_df_para_csv(
    df: pd.DataFrame,
    path_csv: str | Path,
    sep: str = ",",
    encoding: str = "utf-8",
    index: bool = False,
) -> Path:
    """
    Salva um DataFrame como CSV.

    Responsabilidade:
    - apenas escrita
    - nenhuma validação semântica
    - nenhuma transformação
    - cria diretório se necessário
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("O objeto informado não é um pandas.DataFrame.")

    path = Path(path_csv)

    if path.suffix.lower() != ".csv":
        raise ValueError("O arquivo deve ter extensão .csv.")

    # garante que o diretório existe
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        df.to_csv(
            path,
            sep=sep,
            encoding=encoding,
            index=index,
        )
    except Exception as e:
        raise IOError(f"Erro ao salvar CSV: {e}")

    return path

