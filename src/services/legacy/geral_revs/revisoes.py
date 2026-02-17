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

def aplicar_revisao_nomes(
        df_original: pd.DataFrame,
        df_logs: pd.DataFrame,
        coluna_nome: str
) -> pd.DataFrame:
    """
    Aplica revisões de nomes ao DataFrame original com base
    no DataFrame de logs de revisão.

    Atualiza somente quando valor_revisado é válido (não vazio).
    """

    if not isinstance(df_original, pd.DataFrame):
        raise TypeError("df_original deve ser um DataFrame")

    if not isinstance(df_logs, pd.DataFrame):
        raise TypeError("df_logs deve ser um DataFrame")

    if coluna_nome not in df_original.columns:
        raise KeyError(f"Coluna '{coluna_nome}' não encontrada no df_original")

    for col in ["id_registro", "valor_revisado"]:
        if col not in df_logs.columns:
            raise KeyError(f"Coluna '{col}' não encontrada no df_logs")

    df_final = df_original.copy()

    for _, row in df_logs.iterrows():
        idx = row["id_registro"]
        valor_revisado = row["valor_revisado"]

        if idx not in df_final.index:
            continue

        # Se não for string ou for nulo → limpa a célula
        if not isinstance(valor_revisado, str):
            df_final.at[idx, coluna_nome] = pd.NA
            continue

        valor_limpo = valor_revisado.strip()

        # Se string vazia após strip → limpa
        if valor_limpo == "":
            df_final.at[idx, coluna_nome] = pd.NA
        else:
            df_final.at[idx, coluna_nome] = valor_limpo

    return df_final