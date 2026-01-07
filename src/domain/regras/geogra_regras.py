from src.domain.vocabulario.voc_geografia import *
from typing import Optional


def classificar_regiao_estado(valor: str) -> Optional[str]:
    """
    Recebe nome ou sigla de um estado brasileiro e retorna a região correspondente.
    """

    if not isinstance(valor, str):
        return None

    valor = valor.strip().upper()

    if not valor:
        return None

    # ======================================================
    # Caso 1 — sigla (UF)
    # ======================================================
    if valor in regiao_por_uf:
        return regiao_por_uf[valor]

    # ======================================================
    # Caso 2 — nome completo do estado
    # ======================================================
    uf = nome_para_uf.get(valor)
    if uf:
        return regiao_por_uf.get(uf)

    return None
