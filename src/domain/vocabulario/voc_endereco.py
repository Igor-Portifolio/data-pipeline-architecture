# =========================================================
# VOCABULÁRIO CANÔNICO DE ENDEREÇOS
# =========================================================
# Regra:
# - CHAVE = forma canônica (sempre MAIÚSCULA)
# - VALOR = conjunto de variações aceitas (minúsculas, sem ponto)
# - Sempre EXPANDIR, nunca abreviar
# =========================================================


# ---------------------------------------------------------
# TIPOS DE LOGRADOURO
# ---------------------------------------------------------
LOGRADOUROS = {
    "RUA": {"rua"},
    "AVENIDA": {"av", "av.", "avenida"},
    "ALAMEDA": {"al", "alameda"},
    "TRAVESSA": {"trav", "travessa"},
    "ESTRADA": {"est", "estrada"},
    "RODOVIA": {"rod", "rodovia"},
    "PRAÇA": {"praca", "praça", "pca", "pça"},
    "LARGO": {"largo"},
    "VIA": {"via"},
    "CONJUNTO": {"conj", "conjunto"},
}

# ---------------------------------------------------------
# UNIDADES PREDIAIS
# ---------------------------------------------------------
UNIDADES = {
    "APARTAMENTO": {"ap", "apt", "apto", "apartamento", "aapt", },
    "ANDAR": {"and", "andar"},
    "BLOCO": {"bl", "bloco"},
    "CASA": {"casa"},
    "SALA": {"sl", "sala"},
    "LOJA": {"lj", "loja"},
    "CONJUNTO": {"conj", "conjunto"},
    "LOTE": {"lt", "lote"},
    "QUADRA": {"qd", "quadra"},
}

# ---------------------------------------------------------
# COMPLEMENTOS ESPACIAIS
# ---------------------------------------------------------
COMPLEMENTOS = {
    "FUNDOS": {"fundos", "fds", "fd"},
    "FRENTE": {"frente", "frt"},
    "TÉRREO": {"terreo", "térreo"},
    "SUBSOLO": {"subsolo"},
    "COBERTURA": {"cobertura"},
    "ESQUINA": {"esquina"},
    "ANEXO": {"anexo"},
}

# ---------------------------------------------------------
# INDICADORES DE AUSÊNCIA / EXCEÇÃO
# ---------------------------------------------------------
EXCECOES = {
    "SEM_NUMERO": {"s/n", "sn", "sem numero", "sem número"},
    "NAO_INFORMADO": {"nao informado", "não informado", "n/i"},
}

# ---------------------------------------------------------
# AGRUPAMENTO GERAL (ÚTIL PARA BUSCA)
# ---------------------------------------------------------
VOCABULARIO_ENDERECO = {
    "LOGRADOURO": LOGRADOUROS,
    "UNIDADE": UNIDADES,
    "COMPLEMENTO": COMPLEMENTOS,
    "EXCECAO": EXCECOES,
}

VOCABULARIO_BAIRRO = {
    # Núcleos urbanos
    "JD": "JARDIM",
    "JARD": "JARDIM",
    "JDIM": "JARDIM",

    "VL": "VILA",
    "VLA": "VILA",

    "PQ": "PARQUE",
    "PQUE": "PARQUE",

    "CONJ": "CONJUNTO",
    "CJ": "CONJUNTO",

    "LOT": "LOTEAMENTO",
    "LOTEAM": "LOTEAMENTO",

    "RES": "RESIDENCIAL",
    "RESID": "RESIDENCIAL",

    # Santos / religiosos
    "STA": "SANTA",
    "ST": "SANTO",
    "STO": "SANTO",
    "STA.": "SANTA",
    "STO.": "SANTO",

    # Direções / regiões
    "JD.": "JARDIM",
    "VL.": "VILA",
    "PQ.": "PARQUE",

    # Termos frequentes
    "CENT": "CENTRO",
    "CTR": "CENTRO",

    "IND": "INDUSTRIAL",
    "INDUST": "INDUSTRIAL",

    # Condomínios
    "COND": "CONDOMINIO",
    "CONDOM": "CONDOMINIO",

    # Outros
    "HAB": "HABITACIONAL",
    "HABIT": "HABITACIONAL",

    "EST": "ESTANCIA",
    "EST.": "ESTANCIA",
}
