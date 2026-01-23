import pandas as pd



def aplicar_revisao_manual(
    df_principal: pd.DataFrame,
    df_revisao: pd.DataFrame,
    nome_coluna_df: str,
) -> pd.DataFrame:
    """
    Aplica valores revisados (humanos) ao DataFrame principal
    usando id_registro como chave.
    """

    # -------------------------------
    # Validações mínimas
    # -------------------------------
    colunas_revisao = {"id_registro", "valor_revisado"}
    if not colunas_revisao.issubset(df_revisao.columns):
        raise KeyError(
            f"df_revisao deve conter as colunas {colunas_revisao}"
        )

    if "id_registro" not in df_principal.columns:
        raise KeyError("df_principal deve conter a coluna 'id_registro'.")

    if nome_coluna_df not in df_principal.columns:
        raise KeyError(
            f"Coluna '{nome_coluna_df}' não encontrada no df_principal."
        )

    df_saida = df_principal.copy()

    # -------------------------------
    # Indexa revisão por id_registro
    # -------------------------------
    mapa_revisao = (
        df_revisao
        .set_index("id_registro")["valor_revisado"]
    )

    # -------------------------------
    # Aplica sobrescrita controlada
    # -------------------------------
    for idx, valor in mapa_revisao.items():
        if pd.notna(valor) and idx in df_saida["id_registro"].values:
            df_saida.loc[
                df_saida["id_registro"] == idx,
                nome_coluna_df
            ] = valor

    return df_saida
