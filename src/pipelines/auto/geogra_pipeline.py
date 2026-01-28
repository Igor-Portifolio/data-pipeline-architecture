import pandas as pd
from src.services.geografia import *

def geogra_pipeline(
    df: pd.DataFrame,
    coluna_estado: str
) -> pd.DataFrame:
    """
    Pipeline geográfico:
    - Classifica estados em regiões
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    classificador = ClassificadorRegiao(df)

    classificador.adicionar_regiao(coluna_estado)

    return classificador.df
