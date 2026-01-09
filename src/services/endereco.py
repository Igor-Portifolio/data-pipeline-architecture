import pandas as pd
from src.domain.regras.endereco_regras import *

class NormalizadorEndereco:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def normalizar_coluna_endereco(self, coluna: str) -> pd.DataFrame:
        """
        Aplica a normalização de endereço em uma coluna do DataFrame,
        sobrescrevendo os valores originais.
        """

        if coluna not in self.df.columns:
            raise KeyError(f"Coluna '{coluna}' não encontrada.")

        self.df[coluna] = self.df[coluna].apply(normalizar_endereco_texto)

        return self.df
