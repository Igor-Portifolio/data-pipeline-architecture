from src.domain.regras.age_and_date import *


class AgeClassifier:
    def __init__(self, df: pd.DataFrame, ):
        self.df = df.copy()

    def adicionar_faixa_etaria(
            self,
            coluna_data_nascimento: str
    ) -> pd.DataFrame:
        """
        Adiciona uma coluna de faixa etária com base na data de nascimento.
        """

        if coluna_data_nascimento not in self.df.columns:
            raise KeyError(
                f"Coluna '{coluna_data_nascimento}' não encontrada no DataFrame."
            )

        # Calcula faixa etária
        faixa_etaria = self.df[coluna_data_nascimento].apply(
            categorizar_data_nascimento
        )

        nome_coluna = "faixa_etaria"

        # Insere a coluna logo após a data de nascimento
        idx = self.df.columns.get_loc(coluna_data_nascimento) + 1
        self.df.insert(idx, nome_coluna, faixa_etaria)

        return self.df

    def adicionar_decada(
            self,
            coluna_data: str
    ) -> pd.DataFrame:
        """
        Adiciona uma coluna 'decada' (intervalo de ano)
        ao lado da coluna de data informada.
        """

        if coluna_data not in self.df.columns:
            raise KeyError(
                f"Coluna '{coluna_data}' não encontrada no DataFrame."
            )

        # aplica a função de domínio
        decadas = self.df[coluna_data].apply(
            classificar_intervalo_ano
        )

        idx = self.df.columns.get_loc(coluna_data) + 1
        self.df.insert(idx, "decada", decadas)

        return self.df




