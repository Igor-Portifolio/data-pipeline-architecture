from typing import Literal
import pandas as pd
from src.domain.age_groups import *
from datetime import date, datetime
from typing import Optional
from datetime import date, datetime


def categorizar_data_nascimento(data_nascimento):
    """
    Recebe uma data de nascimento e retorna a categoria etária.
    """

    if pd.isna(data_nascimento):
        raise ValueError("Data de nascimento inválida: valor nulo.")

    # ======================================================
    # 1. Converter para date
    # ======================================================
    if isinstance(data_nascimento, datetime):
        data_nascimento = data_nascimento.date()

    elif isinstance(data_nascimento, date):
        pass

    elif isinstance(data_nascimento, str):
        try:
            data_nascimento = pd.to_datetime(data_nascimento).date()
        except Exception:
            raise ValueError(f"Data de nascimento inválida: {data_nascimento}")

    else:
        raise ValueError(f"Tipo inválido para data de nascimento: {type(data_nascimento)}")

    hoje = date.today()

    if data_nascimento > hoje:
        raise ValueError(
            f"Data de nascimento no futuro: {data_nascimento}"
        )

    # ======================================================
    # 2. Calcular idade (anos completos)
    # ======================================================
    idade = hoje.year - data_nascimento.year

    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    if idade < 0:
        raise ValueError(f"Idade inválida calculada: {idade}")

    # ======================================================
    # 3. Categorizar idade
    # ======================================================
    categoria = pd.cut(
        x=[idade],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        right=True,
        include_lowest=True
    )[0]

    return str(categoria)

def classificar_intervalo_ano(valor) -> Optional[str]:
    """
    Classifica uma data ou ano em um intervalo semântico pré-definido.
    """

    # ======================================================
    # 1. Extrair ano
    # ======================================================
    ano = None

    if isinstance(valor, int):
        ano = valor

    elif isinstance(valor, (date, datetime)):
        ano = valor.year

    elif isinstance(valor, str):
        valor = valor.strip()

        # tenta pegar ano em formatos comuns
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y"):
            try:
                ano = datetime.strptime(valor, fmt).year
                break
            except ValueError:
                continue

    if ano is None or ano < 0:
        return None

    # ======================================================
    # 2. Classificar no bin correto
    # ======================================================
    for i in range(len(YEAR_BINS) - 1):
        inicio = YEAR_BINS[i]
        fim = YEAR_BINS[i + 1]

        if inicio < ano <= fim:
            return YEAR_RANGE_LABELS[i]

    return None


