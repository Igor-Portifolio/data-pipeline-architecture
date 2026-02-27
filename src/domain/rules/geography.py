from src.domain.vocabulary.geography import regiao_por_uf, nome_para_uf
from typing import Optional


def classify_state_region(value: str) -> Optional[str]:
    """
    Return the Brazilian region corresponding to a given state name
    or state code (UF).

    Args:
        value: State name or two-letter state code.

    Returns:
        The corresponding region if found, otherwise None.
    """
    if not isinstance(value, str):
        return None

    value = value.strip().upper()
    if not value:
        return None

    if value in regiao_por_uf:
        return regiao_por_uf[value]

    uf = nome_para_uf.get(value)
    if uf:
        return regiao_por_uf.get(uf)

    return None