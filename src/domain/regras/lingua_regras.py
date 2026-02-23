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

    # tokeniza por espaços (colapsa múltiplos espaços)
    partes = [p for p in valor_normalizado.split() if p]

    # REGRA 1 — "nome longo" por token (só se tiver 2+ palavras)
    # ajuste o limiar conforme seu dado real
    LIMIAR_TOKEN = 12

    if any(len(p) >= LIMIAR_TOKEN for p in partes):
        flags.append("NOME_LONGO")

    # REGRA 2 — domínio de e-mail
    for dominio in DOMINIOS_EMAIL_COMUNS:
        if dominio in valor_normalizado:
            flags.append("DOMINIO_EMAIL")
            break

    return flags

def remover_termos_invalidos(texto: str) -> str:
    if not isinstance(texto, str):
        return ""

    termos_invalidos = (
        set(titulos_profissoes)
        | set(partidos_politicos)
        | set(universidades_federais)
        | set(ufs_brasil)
    )

    if not termos_invalidos:
        return texto.strip()

    padrao = r"\b(" + "|".join(re.escape(t) for t in termos_invalidos) + r")\.?\b"

    texto_limpo = re.sub(padrao, "", texto, flags=re.IGNORECASE)
    texto_limpo = re.sub(r"\s{2,}", " ", texto_limpo).strip()

    return texto_limpo

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

def pipeline_limpar_nome_domain(texto: str):
    """
    Dado um texto cru, retorna nome limpo ou pd.NA.
    """

    if not isinstance(texto, str):
        return pd.NA

    texto = texto.strip()

    texto = remover_termos_invalidos(texto)
    texto = normalizar_caracteres_nome(texto)

    if eh_nome_linguisticamente_invalido(texto):
        return pd.NA

    if not texto_tem_letras(texto):
        return pd.NA

    return texto


