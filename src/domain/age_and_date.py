from typing import Literal
import pandas as pd
from src.domain.age_groups import *

def categorize_age(age: int | float):

    if age < 0 or pd.isna(age):
        raise ValueError(f"Idade inválida: {age}. Deve ser maior ou igual a 0.")

    # pandas.cut é a forma mais segura e legível para binning
    category = pd.cut(
        x=[age],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        right=True,      # inclui o limite superior (ex: 24 vai para "18-24")
        include_lowest=True
    )[0]

    # Garante que sempre retornamos uma string válida
    return str(category)

