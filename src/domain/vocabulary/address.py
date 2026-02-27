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

# ---------------------------------------------------------
# TIPOLOGIA URBANA
# ---------------------------------------------------------
TIPOLOGIAS_URBANAS = {
    "JARDIM": {"jd", "jard", "jdim", "jd."},
    "VILA": {"vl", "vla", "vl."},
    "PARQUE": {"pq", "pque", "pq."},
    "LOTEAMENTO": {"lot", "loteam"},
    "ESTANCIA": {"est", "est."},
}

# ---------------------------------------------------------
# ENTIDADES HABITACIONAIS / INSTITUCIONAIS
# ---------------------------------------------------------
ENTIDADES_URBANAS = {
    "CONJUNTO": {"conj", "cj"},
    "CONDOMINIO": {"cond", "condom"},
}

# ---------------------------------------------------------
# CLASSIFICACAO FUNCIONAL
# ---------------------------------------------------------
CLASSIFICACOES_FUNCIONAIS = {
    "RESIDENCIAL": {"res", "resid"},
    "HABITACIONAL": {"hab", "habit"},
    "INDUSTRIAL": {"ind", "indust"},
}

# ---------------------------------------------------------
# MARCADORES GEOGRAFICOS / ADMINISTRATIVOS
# ---------------------------------------------------------
MARCADORES_GEOGRAFICOS = {
    "CENTRO": {"cent", "ctr"},
}

# ---------------------------------------------------------
# QUALIFICADORES RELIGIOSOS / CULTURAIS
# ---------------------------------------------------------
QUALIFICADORES_RELIGIOSOS = {
    "SANTA": {"sta", "sta."},
    "SANTO": {"st", "sto", "sto."},
}

# ---------------------------------------------------------
# AGRUPAMENTO GERAL (ÚTIL PARA PIPELINE / BUSCA)
# ---------------------------------------------------------
VOCABULARIO_BAIRRO = {
    "TIPOLOGIA": TIPOLOGIAS_URBANAS,
    "ENTIDADE": ENTIDADES_URBANAS,
    "CLASSIFICACAO": CLASSIFICACOES_FUNCIONAIS,
    "MARCADOR": MARCADORES_GEOGRAFICOS,
    "QUALIFICADOR": QUALIFICADORES_RELIGIOSOS,
}
