import pandas as pd
import re
from datetime import datetime
from typing import Any
from typing import Optional
from typing import List


def ordenar_coluna_alfa(df: pd.DataFrame, coluna: str) -> list[str]:
    """
    Retorna uma lista com os valores da coluna em ordem alfabética.
    """

    if coluna not in df.columns:
        raise KeyError(f"Coluna '{coluna}' não encontrada.")

    # Converte para string para ordenação segura
    valores = df[coluna].astype(str)

    # Ordenação alfabética
    return sorted(valores, key=lambda x: x.strip().upper())


def valores_unicos(lista: List[str]) -> List[str]:
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


def extrair_coluna_string(df, nome_coluna: str) -> list[str]:
    """
    Extrai uma coluna de um DataFrame e retorna seus valores como lista de strings.

    Levanta erro se a coluna não existir ou se não for composta por strings.
    """
    if nome_coluna not in df.columns:
        raise KeyError(f"Coluna '{nome_coluna}' não existe no DataFrame")

    serie = df[nome_coluna]

    if not all(isinstance(valor, str) for valor in serie.dropna()):
        raise TypeError(f"Coluna '{nome_coluna}' não é composta exclusivamente por strings")

    return serie.tolist()


def substituir_por_grupos(
        df: pd.DataFrame,
        coluna: str,
        grupos_origem: List[List[str]],
        grupos_destino: List[List[str]],
) -> pd.DataFrame:
    if len(grupos_origem) != len(grupos_destino):
        raise ValueError("grupos_origem e grupos_destino devem ter o mesmo tamanho")

    mapa_substituicao: dict[str, str] = {}

    for origem, destino in zip(grupos_origem, grupos_destino):
        if len(destino) != 1:
            raise ValueError("Cada grupo de destino deve ter dimensão 1")

        if len(origem) == 1:
            continue  # identidade → não faz nada

        valor_destino = destino[0]

        for valor in origem:
            mapa_substituicao[valor] = valor_destino

    df_out = df.copy()
    df_out[coluna] = df_out[coluna].replace(mapa_substituicao)

    return df_out
