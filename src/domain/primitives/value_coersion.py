import pandas as pd
import re
from datetime import datetime
from typing import Any
from src.domain.vocabulary.symbols import SUPERSCRIPT_MAP


def coerce_value(valor: Any) -> Any:
    """
    Coerce a scalar value into int, float, or datetime when possible.

    Rules:
        - None and empty strings become pd.NA.
        - Numeric inputs (int/float) are returned as-is.
        - Non-string, non-numeric inputs are returned as-is.
        - Strings are stripped and then tested in order:
            1) explicit date formats
            2) monetary/numeric patterns (BR and international)
            3) integer / float parsing
        - Fallback returns the stripped string.

    Args:
        valor: Input scalar value.

    Returns:
        The coerced value (int, float, datetime, pd.NA, or original/fallback value).
    """

    if valor is None:
        return pd.NA

    if isinstance(valor, (int, float)):
        return valor

    if not isinstance(valor, str):
        return valor

    texto = valor.strip()

    if texto == "":
        return pd.NA

    formatos_data: tuple[str, ...] = ("%d/%m/%Y", "%Y-%m-%d", "%Y%m%d")

    for fmt in formatos_data:
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            continue

    texto_num = re.sub(r"[R$\s]", "", texto)

    texto_num = texto_num.translate(SUPERSCRIPT_MAP)

    if re.fullmatch(r"\d{1,3}(\.\d{3})*,\d+", texto_num):
        texto_num = texto_num.replace(".", "").replace(",", ".")
        return float(texto_num)

    if re.fullmatch(r"\d{1,3}(,\d{3})*\.\d+", texto_num):
        texto_num = texto_num.replace(",", "")
        return float(texto_num)

    if texto_num.isdigit():
        return int(texto_num)

    try:
        return float(texto_num)
    except ValueError:
        return texto
