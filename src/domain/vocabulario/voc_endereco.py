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
    "RUA": {"r", "rua"},
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
    "APARTAMENTO": {"ap", "apt", "apto", "apartamento"},
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
    "FUNDOS": {"fundos"},
    "FRENTE": {"frente"},
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
