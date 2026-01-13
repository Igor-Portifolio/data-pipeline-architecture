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

    def normalizar_coluna_bairro(self, coluna: str) -> pd.DataFrame:
        """
        Aplica a normalização de bairro em uma coluna do DataFrame,
        sobrescrevendo os valores originais.
        """

        if coluna not in self.df.columns:
            raise KeyError(f"Coluna '{coluna}' não encontrada.")

        self.df[coluna] = self.df[coluna].apply(normalizar_bairro_texto)

        return self.df

    def separar_bairros_por_estado(
            self,
            coluna_bairro: str,
            coluna_estado: str
    ) -> dict[str, pd.DataFrame]:
        """
        Separa o DataFrame em múltiplos DataFrames por estado,
        preservando rastreabilidade para revisão manual.
        """

        if coluna_bairro not in self.df.columns:
            raise KeyError(f"Coluna '{coluna_bairro}' não encontrada.")

        if coluna_estado not in self.df.columns:
            raise KeyError(f"Coluna '{coluna_estado}' não encontrada.")

        resultado: dict[str, pd.DataFrame] = {}

        # garante que o índice original seja preservado
        df_base = self.df.copy()

        for estado, df_estado in df_base.groupby(coluna_estado):
            df_saida = pd.DataFrame({
                "row_id": df_estado.index,
                "estado": estado,
                "bairro_original": df_estado[coluna_bairro].values,
                "bairro_normalizado": [""] * len(df_estado),
            })

            resultado[str(estado)] = df_saida.reset_index(drop=True)

        return resultado

    def ordenar_coluna_alfa(self, coluna: str) -> list[str]:
        """
        Retorna uma lista com os valores da coluna em ordem alfabética.
        """

        if coluna not in self.df.columns:
            raise KeyError(f"Coluna '{coluna}' não encontrada.")

        # Converte para string para ordenação segura
        valores = self.df[coluna].astype(str)

        # Ordenação alfabética
        return sorted(valores, key=lambda x: x.strip().upper())

    def valores_unicos(self, lista: List[str]) -> List[str]:
        """
        Recebe uma lista de strings e retorna os valores únicos,
        preservando a ordem de primeira ocorrência.
        """

        if not isinstance(lista, list):
            return []

        vistos = set()
        resultado = []

        for item in lista:
            if item not in vistos:
                vistos.add(item)
                resultado.append(item)

        return resultado
