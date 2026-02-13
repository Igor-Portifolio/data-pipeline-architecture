from src.domain.vocabulario.voc_geografia import *
from src.domain.regras.endereco_regras import *
from src.infra.io.readers import *
from typing import List


def preparar_df_ibge(
        df_ibge: pd.DataFrame
) -> pd.DataFrame:
    """
    Prepara o DataFrame do IBGE no formato padrão do sistema.
    Retorna apenas as colunas relevantes.
    """

    colunas_necessarias = [
        "NM_REGIAO",
        "NM_UF",
        "NM_MUN",
        "NM_BAIRRO",
    ]

    faltantes = [c for c in colunas_necessarias if c not in df_ibge.columns]
    if faltantes:
        raise KeyError(f"Colunas ausentes no DF do IBGE: {faltantes}")

    df_saida = df_ibge[colunas_necessarias].copy()

    return df_saida


def adicionar_sigla_uf(
        df: pd.DataFrame
) -> pd.DataFrame:
    """
    Adiciona a coluna SIGLA_UF ao lado de NM_UF,
    baseada no dicionário nome_para_uf.
    """

    if "NM_UF" not in df.columns:
        raise KeyError("Coluna 'NM_UF' não encontrada no DataFrame.")

    df_saida = df.copy()

    # normaliza para lookup
    uf_normalizada = (
        df_saida["NM_UF"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df_saida["SIGLA_UF"] = uf_normalizada.map(nome_para_uf)

    # reorganiza colunas para SIGLA_UF ficar ao lado de NM_UF
    cols = list(df_saida.columns)
    idx = cols.index("NM_UF")

    cols.insert(idx + 1, cols.pop(cols.index("SIGLA_UF")))
    df_saida = df_saida[cols]

    return df_saida






def listar_bairros_canonicos_sqlite(
    db_path: str,
    table_name: str,
    query: str | None = None
) -> List[str]:
    """
    Consulta o SQLite e retorna uma lista de bairros canônicos (únicos).

    Camada: Service
    """

    df = consultar_df_sqlite(
        db_path=db_path,
        table_name=table_name,
        query=query
    )

    if df.empty:
        return []

    if "NM_BAIRRO" not in df.columns:
        raise KeyError("Coluna 'NM_BAIRRO' não encontrada no DataFrame.")

    bairros = (
        df["NM_BAIRRO"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    # remove duplicados preservando ordem
    bairros_unicos = list(dict.fromkeys(bairros))

    return bairros_unicos


def resolver_bairros_por_referencia_ibge(
    bairros: List[str],
    uf: str,
    db_path: str,
    table_name: str,
) -> List[List[str]]:
    """
    Orquestra a resolução de bairros usando base canônica do IBGE.

    Etapas:
    1. Busca bairros canônicos do IBGE (SQLite)
    2. Agrupa bairros similares da entrada
    3. Resolve melhor match por grupo
    """

    if not bairros:
        return []

    # --------------------------------------------------
    # 1️⃣ Buscar bairros canônicos do IBGE (por UF)
    # --------------------------------------------------
    query = f"SIGLA_UF = '{uf}'"

    bairros_ibge = listar_bairros_canonicos_sqlite(
        db_path=db_path,
        table_name=table_name,
        query=query
    )

    if not bairros_ibge:
        # Sem referência → retorna grupos vazios
        return [[b] for b in bairros]

    # --------------------------------------------------
    # 2️⃣ Agrupar bairros similares da entrada
    # --------------------------------------------------
    grupos = group_similar_bairros(
        bairros=bairros,
        prefix_length=3,
        jaro_threshold=0.88
    )

    # --------------------------------------------------
    # 3️⃣ Resolver melhor match por grupo
    # --------------------------------------------------
    resultado = escolher_melhor_match(
        grupos=grupos,
        candidatos=bairros_ibge,
        limiar_alto=0.9
    )

    return resultado


