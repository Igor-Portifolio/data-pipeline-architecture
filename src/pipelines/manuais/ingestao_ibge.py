from src.services.geral_subjects.ibge_service import *


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