import pandas as pd
import re
from datetime import datetime
from typing import Any

from typing import Optional


def coerce_value(valor: Any):
    """
    Tenta converter um valor para int, float ou datetime.
    Fallback: string normalizada.
    """

    if pd.isna(valor):
        return pd.NA

    # já numérico
    if isinstance(valor, (int, float)):
        return valor

    if not isinstance(valor, str):
        return valor

    texto = valor.strip()

    if texto == "":
        return pd.NA

    # ======================================================
    # 1️⃣ Datas explícitas
    # ======================================================
    formatos_data = ("%d/%m/%Y", "%Y-%m-%d", "%Y%m%d")

    for fmt in formatos_data:
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            pass

    # ======================================================
    # 2️⃣ Valores monetários / numéricos
    # ======================================================

    # remove símbolo de moeda
    texto_num = re.sub(r"[R$\s]", "", texto)

    # padrão brasileiro: 1.234,56
    if re.fullmatch(r"\d{1,3}(\.\d{3})*,\d+", texto_num):
        texto_num = texto_num.replace(".", "").replace(",", ".")
        return float(texto_num)

    # padrão internacional: 1,234.56
    if re.fullmatch(r"\d{1,3}(,\d{3})*\.\d+", texto_num):
        texto_num = texto_num.replace(",", "")
        return float(texto_num)

    # inteiro simples
    if texto_num.isdigit():
        return int(texto_num)

    # float simples
    try:
        return float(texto_num)
    except ValueError:
        pass

    # ======================================================
    # 3️⃣ Fallback
    # ======================================================
    return texto


def trim_whitespace_value(valor: Any):
    """
    Remove whitespace periférico e invisível de strings ou listas de strings.
    """

    if pd.isna(valor):
        return valor

    # ======================================================
    # Caso 1 — string
    # ======================================================
    if isinstance(valor, str):
        texto = valor

        # normaliza whitespace invisível (inclui \u00A0)
        texto = re.sub(r"[\s\u00A0]+", " ", texto)

        return texto.strip()

    # ======================================================
    # Caso 2 — lista de strings
    # ======================================================
    if isinstance(valor, list):
        return [
            trim_whitespace_value(v)
            for v in valor
            if not (isinstance(v, str) and v.strip() == "")
        ]

    return valor


def normalizar_pontuacao_texto(texto: str) -> Optional[str]:
    """
    Remove pontuação e mantém apenas letras, espaços e apóstrofo
    (apóstrofo válido apenas no meio da palavra).
    """

    if not isinstance(texto, str):
        return None

    texto = texto.strip()

    if not texto:
        return None

    # ======================================================
    # 1️⃣ Remove toda pontuação exceto apóstrofo
    # ======================================================
    texto = re.sub(r"[^\w\sÀ-ÿ']", " ", texto)

    # ======================================================
    # 2️⃣ Remove underscores deixados por \w
    # ======================================================
    texto = texto.replace("_", " ")

    # ======================================================
    # 3️⃣ Remove apóstrofo no início ou fim da palavra
    # ======================================================
    texto = re.sub(r"\b'+", "", texto)
    texto = re.sub(r"'+\b", "", texto)

    # ======================================================
    # 4️⃣ Normaliza espaços
    # ======================================================
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto if texto else None

