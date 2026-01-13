import pandas as pd
from src.domain.vocabulario.voc_geografia import *
from typing import Optional
from src.infra.sql_writer import *
from src.infra.readers import *

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


def ingestao_ibge_sqlite(
        path_gpkg: str,
        db_path: str,
        table_name: str,
        regiao_por_uf: Optional[dict] = None,
) -> None:
    """
    Pipeline principal de ingestão do IBGE para SQLite.

    Etapas:
    1. Leitura do GPKG (Infra)
    2. Preparação estrutural do DataFrame
    3. Enriquecimento com SIGLA_UF (e região, se fornecido)
    4. Persistência no SQLite (Infra)
    """

    # ======================================================
    # 1️⃣ Ler GPKG (Infra)
    # ======================================================
    df_bruto = ler_arquivo_gpkg(path_gpkg)

    # ======================================================
    # 2️⃣ Preparar DataFrame (Service / Adapter)
    # ======================================================
    df_preparado = preparar_df_ibge(df_bruto)

    # ======================================================
    # 3️⃣ Enriquecer com SIGLA_UF
    # ======================================================
    df_enriquecido = adicionar_sigla_uf(df_preparado)

    # ======================================================
    # 4️⃣ Enriquecer com REGIÃO (opcional)
    # ======================================================
    if regiao_por_uf is not None:
        if "SIGLA_UF" not in df_enriquecido.columns:
            raise KeyError("Coluna 'SIGLA_UF' necessária para mapear região.")

        df_enriquecido = df_enriquecido.copy()
        df_enriquecido["REGIAO"] = df_enriquecido["SIGLA_UF"].map(regiao_por_uf)

    # ======================================================
    # 5️⃣ Persistir no SQLite (Infra)
    # ======================================================
    salvar_df_sqlite(
        df=df_enriquecido,
        db_path=db_path,
        table_name=table_name,
        modo="replace"
    )
