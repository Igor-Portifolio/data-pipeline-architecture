import pandas as pd
from src.domain.regras.geogra_regras import *

class ClassificadorRegiao:

        def __init__(self, df: pd.DataFrame, ):
            self.df = df.copy()

        def adicionar_regiao(self, coluna_estado: str) -> pd.DataFrame:
            """
            Adiciona uma coluna 'Regioes' ao lado da coluna de estados,
            classificando cada valor via classificar_regiao_estado.
            """

            if coluna_estado not in self.df.columns:
                raise KeyError(f"Coluna '{coluna_estado}' não encontrada.")

            # aplica a função pura
            regioes = self.df[coluna_estado].apply(classificar_regiao_estado)

            # posição da nova coluna (logo após a coluna de estado)
            idx = self.df.columns.get_loc(coluna_estado) + 1

            self.df.insert(idx, "Regioes", regioes)

            return self.df