from src.services.geral_subjects.endereco import *

def endereco_pipeline(
        df: pd.DataFrame,
        coluna: str
) -> pd.DataFrame:
    """
    Pipeline de normalização de endereço para uma coluna específica.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    normalizador = NormalizadorEndereco(df)

    normalizador.normalizar_coluna_endereco(coluna)

    return normalizador.df