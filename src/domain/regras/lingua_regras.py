from src.domain.vocabulario.voc_lingua import *
import re
from typing import List
import pandas as pd

def classificar_string_simples(valor: str) -> List[str]:
    """
    Classifica uma string simples com base em regras heurísticas.

    Regras:
    - Se tiver mais de 9 caracteres -> NOME_LONGO
    - Se contiver domínio de e-mail conhecido -> DOMINIO_EMAIL
    """

    if not isinstance(valor, str):
        return []

    valor_normalizado = valor.strip().lower()

    flags: list[str] = []

    # ======================================================
    # REGRA 1 — tamanho do nome
    # ======================================================
    if len(valor_normalizado) > 10:
        flags.append("NOME_LONGO")

    # ======================================================
    # REGRA 2 — domínio de e-mail
    # ======================================================
    for dominio in DOMINIOS_EMAIL_COMUNS:
        if dominio in valor_normalizado:
            flags.append("DOMINIO_EMAIL")
            break

    return flags

def remover_titulos_e_profissoes(texto: str) -> str:
    if not isinstance(texto, str):
        return ""

    padrao = r"\b(" + "|".join(titulos_profissoes) + r")\.?\b"
    return re.sub(padrao, "", texto, flags=re.IGNORECASE).strip()

def normalizar_caracteres_nome(texto: str) -> str:
    if not isinstance(texto, str):
        return ""

    texto = re.sub(r"[^A-Za-zÀ-ÿ\s']", "", texto)
    texto = re.sub(r"^'+", "", texto)
    texto = re.sub(r"'+$", "", texto)
    texto = re.sub(r"\s+'\s+", " ", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()

def eh_nome_linguisticamente_invalido(texto: str) -> bool:
    if not isinstance(texto, str):
        return True

    termos_invalidos = (
        RELACOES_FAMILIARES
        | ENTIDADES_RELIGIOSAS
        | FRASES_RELIGIOSAS
        | RESPOSTAS_INVALIDAS
        | TOKENS_INVALIDOS_SOLOS
    )

    padrao = r"\b(" + "|".join(re.escape(t) for t in termos_invalidos) + r")\b"

    return bool(re.search(padrao, texto, flags=re.IGNORECASE))

def texto_tem_letras(texto: str) -> bool:
    if not isinstance(texto, str):
        return False

    return bool(re.search(r"[A-Za-zÀ-ÿ]", texto))

def limpar_nome_unitario(texto: str):
    """
    Dado um texto cru, retorna nome limpo ou pd.NA.
    """

    if not isinstance(texto, str):
        return pd.NA

    texto = texto.strip()

    texto = remover_titulos_e_profissoes(texto)
    texto = normalizar_caracteres_nome(texto)

    if eh_nome_linguisticamente_invalido(texto):
        return pd.NA

    if not texto_tem_letras(texto):
        return pd.NA

    return texto


