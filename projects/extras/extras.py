from __future__ import annotations
import re
import pandas as pd
from typing import Iterable, Union, List, Any

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def is_valid_email(value: str) -> bool:
    if not isinstance(value, str):
        return False
    return bool(EMAIL_REGEX.match(value.strip()))


def corrigir_email_em_nome(
        df: pd.DataFrame,
        nome_coluna: str,
        email_coluna: str
) -> pd.DataFrame:
    """
    Se o valor em nome_coluna for um email válido,
    e email_coluna estiver vazia, preenche email_coluna
    com o valor encontrado no nome.
    """

    if nome_coluna not in df.columns:
        raise KeyError(f"Coluna '{nome_coluna}' não encontrada no DataFrame.")

    if email_coluna not in df.columns:
        raise KeyError(f"Coluna '{email_coluna}' não encontrada no DataFrame.")

    # Identifica linhas onde nome é um email válido
    mask_nome_is_email = df[nome_coluna].apply(is_valid_email)

    # Identifica linhas onde email_coluna está vazia ou nula
    mask_email_vazio = df[email_coluna].isna() | (df[email_coluna].astype(str).str.strip() == "")

    # Condição final:
    # nome é email E email_coluna está vazia
    mask_final = mask_nome_is_email & mask_email_vazio

    # Garante que a coluna de email seja string
    df[email_coluna] = df[email_coluna].astype("string")

    # Preenche apenas nessas linhas
    df.loc[mask_final, email_coluna] = df.loc[mask_final, nome_coluna]

    return df


def preencher_df1_com_df2(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        coluna_alvo: Union[str, List[str]],
        coluna_mod: Union[str, List[str]],
        coluna_check: str,
) -> pd.DataFrame:
    """
    Preenche df1 com valores de df2 quando:
      - a(s) coluna(s) alvo (chave) batem entre df1 e df2
      - e, para cada coluna em coluna_mod:
          df1[col] está vazia (NaN ou string vazia/espacos)
          e df2[col] tem valor (não NaN e não string vazia/espacos)

    Retorna um novo DataFrame (não modifica df1 in-place).
    """

    keys = [coluna_alvo] if isinstance(coluna_alvo, str) else list(coluna_alvo)
    mods = [coluna_mod] if isinstance(coluna_mod, str) else list(coluna_mod)

    # validações básicas
    missing1 = [c for c in keys + mods if c not in df1.columns]
    missing2 = [c for c in keys + mods if c not in df2.columns]
    if missing1:
        raise KeyError(f"df1 não possui as colunas: {missing1}")
    if missing2:
        raise KeyError(f"df2 não possui as colunas: {missing2}")

    out = df1.copy()

    # reduz df2 para chaves + colunas a trazer e remove duplicatas na chave (mantém a primeira)
    df2_small = df2[keys + mods].copy()
    df2_small = df2_small.drop_duplicates(subset=keys, keep="first")

    # merge para alinhar valores do df2 na mesma linha do df1
    merged = out.merge(df2_small, on=keys, how="left", suffixes=("", "__df2"))

    def is_empty_series(s: pd.Series) -> pd.Series:
        # vazio = NaN OU string vazia/espacos
        if pd.api.types.is_string_dtype(s) or s.dtype == "object":
            return s.isna() | (s.astype("string").str.strip() == "")
        return s.isna()

    def has_value_series(s: pd.Series) -> pd.Series:
        # tem valor = não NaN E (se string) não vazia
        if pd.api.types.is_string_dtype(s) or s.dtype == "object":
            return s.notna() & (s.astype("string").str.strip() != "")
        return s.notna()

    # máscara global de alteração
    any_change_mask = pd.Series(False, index=merged.index)

    # para cada coluna a modificar, preenche somente onde df1 vazio e df2 tem valor
    for col in mods:
        col_df2 = f"{col}__df2"

        # garante que a coluna existe após merge
        if col_df2 not in merged.columns:
            continue

        mask_df1_empty = is_empty_series(merged[col])
        mask_df2_has = has_value_series(merged[col_df2])

        mask_fill = mask_df1_empty & mask_df2_has

        # acumula alterações
        any_change_mask = any_change_mask | mask_fill

        # garante dtype compatível (evita FutureWarning quando coluna era float por causa de NaN)
        merged[col] = merged[col].astype("string")

        merged.loc[mask_fill, col] = merged.loc[mask_fill, col_df2].astype("string")

    merged[coluna_check] = any_change_mask
    # remove colunas auxiliares do df2
    drop_cols = [f"{c}__df2" for c in mods if f"{c}__df2" in merged.columns]
    merged = merged.drop(columns=drop_cols)

    return merged


def preencher_df1_com_df2_teste(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        coluna_alvo: Union[str, List[str]],
        coluna_mod: Union[str, List[str]],
        coluna_check: str,
) -> pd.DataFrame:
    """
    Preenche df1 com valores de df2 quando:
      - a(s) coluna(s) alvo (chave) batem entre df1 e df2
      - e, para cada coluna em coluna_mod:
          df1[col] está vazia (NaN ou string vazia/espacos)
          e df2[col] tem valor (não NaN e não string vazia/espacos)

    EXTRA (adicionado):
      - Se a chave de df2 NÃO existir em df1, cria uma nova linha no resultado,
        copiando os valores de df2 nas colunas equivalentes (colunas em comum)
        e define coluna_check = False.

    Retorna um novo DataFrame (não modifica df1 in-place).
    """

    keys = [coluna_alvo] if isinstance(coluna_alvo, str) else list(coluna_alvo)
    mods = [coluna_mod] if isinstance(coluna_mod, str) else list(coluna_mod)

    # validações básicas
    missing1 = [c for c in keys + mods if c not in df1.columns]
    missing2 = [c for c in keys + mods if c not in df2.columns]
    if missing1:
        raise KeyError(f"df1 não possui as colunas: {missing1}")
    if missing2:
        raise KeyError(f"df2 não possui as colunas: {missing2}")

    out = df1.copy()

    # reduz df2 para chaves + colunas a trazer e remove duplicatas na chave (mantém a primeira)
    df2_small = df2[keys + mods].copy()
    df2_small = df2_small.drop_duplicates(subset=keys, keep="first")

    # merge para alinhar valores do df2 na mesma linha do df1
    merged = out.merge(df2_small, on=keys, how="left", suffixes=("", "__df2"))

    def is_empty_series(s: pd.Series) -> pd.Series:
        # vazio = NaN OU string vazia/espacos
        if pd.api.types.is_string_dtype(s) or s.dtype == "object":
            return s.isna() | (s.astype("string").str.strip() == "")
        return s.isna()

    def has_value_series(s: pd.Series) -> pd.Series:
        # tem valor = não NaN E (se string) não vazia
        if pd.api.types.is_string_dtype(s) or s.dtype == "object":
            return s.notna() & (s.astype("string").str.strip() != "")
        return s.notna()

    # máscara global de alteração
    any_change_mask = pd.Series(False, index=merged.index)

    # para cada coluna a modificar, preenche somente onde df1 vazio e df2 tem valor
    for col in mods:
        col_df2 = f"{col}__df2"

        # garante que a coluna existe após merge
        if col_df2 not in merged.columns:
            continue

        mask_df1_empty = is_empty_series(merged[col])
        mask_df2_has = has_value_series(merged[col_df2])

        mask_fill = mask_df1_empty & mask_df2_has

        # acumula alterações
        any_change_mask = any_change_mask | mask_fill

        # garante dtype compatível (evita FutureWarning quando coluna era float por causa de NaN)
        merged[col] = merged[col].astype("string")
        merged.loc[mask_fill, col] = merged.loc[mask_fill, col_df2].astype("string")

    merged[coluna_check] = any_change_mask

    # remove colunas auxiliares do df2
    drop_cols = [f"{c}__df2" for c in mods if f"{c}__df2" in merged.columns]
    merged = merged.drop(columns=drop_cols)

    # ----------------------------
    # EXTRA: adicionar linhas de df2 cuja chave não existe em df1
    # (agora trazendo TODAS as colunas comuns, ex: 'nome')
    # ----------------------------

    # colunas comuns entre df1 e df2 (exceto coluna_check)
    common_cols = [c for c in df2.columns if c in out.columns and c != coluna_check]

    df2_common = df2[common_cols].copy()
    df2_common = df2_common.drop_duplicates(subset=keys, keep="first")

    keys_df1 = out[keys].drop_duplicates()

    anti = df2_common.merge(keys_df1, on=keys, how="left", indicator=True)
    df2_unmatched = anti[anti["_merge"] == "left_only"].drop(columns=["_merge"])

    if not df2_unmatched.empty:
        new_rows = pd.DataFrame({c: pd.NA for c in merged.columns}, index=range(len(df2_unmatched)))

        # copia todas as colunas comuns (inclui 'nome' se existir)
        for c in df2_unmatched.columns:
            if c in new_rows.columns:
                new_rows[c] = df2_unmatched[c].values

        new_rows[coluna_check] = False
        merged = pd.concat([merged, new_rows], ignore_index=True)

    return merged


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna uma cópia do DataFrame com os headers:
    - em lowercase
    - sem espaços no início e no fim
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame.")

    out = df.copy()

    out.columns = (
        out.columns
        .astype(str)  # garante que são strings
        .str.strip()  # remove espaços
        .str.lower()  # lowercase
    )

    return out


def _normalize_text(text: Any) -> str:
    """
    Mantém apenas letras e números e coloca em uppercase.
    """
    if not isinstance(text, str):
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", text).upper()


def limpar_coluna_relacionada(
        df: pd.DataFrame,
        coluna_1: str,
        coluna_2: str
) -> pd.DataFrame:
    """
    Se coluna_1 == coluna_2 → limpa coluna_2.
    Se coluna_1 estiver contida em coluna_2 → remove a parte comum.
    Caso contrário → mantém como está.
    """

    if coluna_1 not in df.columns or coluna_2 not in df.columns:
        raise KeyError("Colunas informadas não existem no DataFrame.")

    out = df.copy()

    def processar(row):
        v1 = row[coluna_1]
        v2 = row[coluna_2]

        if not isinstance(v1, str) or not isinstance(v2, str):
            return v2

        norm1 = _normalize_text(v1)
        norm2 = _normalize_text(v2)

        # 1️⃣ iguais
        if norm1 == norm2:
            return ""

        # 2️⃣ coluna_1 contida em coluna_2
        if norm1 and norm1 in norm2:
            # remove texto original de v1 dentro de v2
            # mantendo separadores naturais
            pattern = re.escape(v1)
            novo = re.sub(pattern, "", v2, flags=re.IGNORECASE)
            return novo.strip(" /-,")

        return v2

    out[coluna_2] = out.apply(processar, axis=1)

    return out


from typing import Optional
import pandas as pd


def completar_index(
        df: pd.DataFrame,
        coluna_idx: str,
        *,
        coluna_data: Optional[str] = None,
) -> pd.DataFrame:
    """
    Garante que a coluna de índice sequencial exista e esteja completa.

    Regras:
      - Se coluna_idx não existir -> cria.
      - Se existir -> apenas completa onde for NA.
      - Nunca sobrescreve valores já existentes.
      - Garante unicidade.
      - Respeita ordem cronológica se coluna_data for fornecida.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame original.
    coluna_idx : str
        Nome da coluna de índice sequencial.
    coluna_data : Optional[str]
        Coluna usada para ordenar cronologicamente.

    Returns
    -------
    pd.DataFrame
        Novo DataFrame com index completo.
    """

    if df.empty:
        return df.copy()

    out = df.copy()

    # Ordenação cronológica se fornecida
    if coluna_data:
        if coluna_data not in out.columns:
            raise KeyError(f"Coluna '{coluna_data}' não encontrada.")
        out = out.sort_values(by=coluna_data).reset_index(drop=True)

    # Se não existir, cria como NA
    if coluna_idx not in out.columns:
        out[coluna_idx] = pd.NA

    # Converte para tipo inteiro opcional
    out[coluna_idx] = pd.to_numeric(out[coluna_idx], errors="coerce")

    # Descobre maior índice já existente
    max_existente = out[coluna_idx].dropna().max()

    if pd.isna(max_existente):
        proximo = 1
    else:
        proximo = int(max_existente) + 1

    # Conjunto para garantir unicidade
    existentes = set(out[coluna_idx].dropna().astype(int))

    novos_valores = []

    for valor in out[coluna_idx]:
        if pd.notna(valor):
            novos_valores.append(int(valor))
        else:
            while proximo in existentes:
                proximo += 1
            novos_valores.append(proximo)
            existentes.add(proximo)
            proximo += 1

    out[coluna_idx] = novos_valores

    return out
