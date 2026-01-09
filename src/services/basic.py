import pandas as pd
from src.domain.regras.basic_regras import *



class Basic_clean:

    def __init__(self, df: pd.DataFrame, ):
        self.df = df.copy()

    def normalize_nulls(
            self,
            coluna: str = None,
            nulo: str = None
    ) -> pd.DataFrame:
        """
        Trata valores nulos no DataFrame.

        - coluna=None  → aplica a todas as colunas
        - nulo=None    → converte nulos para NaN
        - nulo="texto" → substitui nulos pela string fornecida
        """

        df = self.df.copy()

        def substituir(serie: pd.Series):
            if nulo is None:
                # deixa em NaN
                return serie.replace(["", " ", "nan", "None"], pd.NA)
            else:
                # substitui nulos pela string
                return serie.replace(["", " ", "nan", "None", pd.NA], nulo)

        # Se nenhuma coluna foi especificada → todas
        if coluna is None:
            for col in df.columns:
                df[col] = substituir(df[col])
        else:
            if coluna not in df.columns:
                raise KeyError(f"Coluna '{coluna}' não encontrada no DataFrame!")

            df[coluna] = substituir(df[coluna])

        # Atualiza self.df e retorna
        self.df = df
        return df

    def drop_exact_duplicates(self) -> pd.DataFrame:

        antes = len(self.df)
        self.df = self.df.drop_duplicates(ignore_index=True).copy()
        removidas = antes - len(self.df)
        return self.df

    def coerce_types(self, coluna: str | None = None) -> pd.DataFrame:
        """
        Força coerção de tipos em uma coluna específica ou no DataFrame inteiro.
        """

        if coluna:
            if coluna not in self.df.columns:
                raise KeyError(f"Coluna '{coluna}' não encontrada.")

            self.df[coluna] = self.df[coluna].apply(coerce_value)

        else:
            for col in self.df.columns:
                self.df[col] = self.df[col].apply(coerce_value)

        return self.df

    def trim_whitespace(self) -> pd.DataFrame:
        """
        Remove whitespace periférico, invisível e redundante
        em todo o DataFrame.
        """

        for col in self.df.columns:
            self.df[col] = self.df[col].apply(trim_whitespace_value)

        return self.df

    def normalizar_pontuacao(
        self,
        coluna: str | None = None
    ) -> pd.DataFrame:
        """
        Aplica a normalização de pontuação em uma coluna específica
        ou em todo o DataFrame.
        """

        def aplicar(valor):
            if isinstance(valor, str):
                return normalizar_pontuacao_texto(valor)
            return valor

        if coluna:
            if coluna not in self.df.columns:
                raise KeyError(f"Coluna '{coluna}' não encontrada.")

            self.df[coluna] = self.df[coluna].apply(aplicar)

        else:
            for col in self.df.columns:
                self.df[col] = self.df[col].apply(aplicar)

        return self.df

