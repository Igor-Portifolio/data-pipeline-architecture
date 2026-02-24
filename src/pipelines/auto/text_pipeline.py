from src.services.text_normalization_service import *
from src.infra.io.writers import *
from src.infra.io.paths import *
from src.services.legacy.geral_revs.revisoes import aplicar_revisao_nomes


def text_basic_pipeline(df: pd.DataFrame,
                        columns_strings: str | list[str],
                        column_email: str | list[str] | None = None,
                        column_name: str | list[str] | None = None,
                        column_cpf: str | None = None,
                        column_tel: str | None = None) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Standard_text(df)
    cleaner.normalize_text(
        colunas=columns_strings,
        upper=True,
        remover_acentos=True
    )

    if column_email is not None:
        if not isinstance(column_email, str) and not isinstance(column_email, list):
            raise ValueError("coluna_email deve ser uma string não vazia quando fornecida.")
        cleaner.normalize_text(
            colunas=column_email,
            lower=True,
        )

    if column_name is not None:
        if not isinstance(column_name, str) and not isinstance(column_name, list):
            raise ValueError("coluna_nome deve ser uma string não vazia quando fornecida.")
        cleaner.remover_emojis_e_simbolos(columns=column_name)

    if column_cpf is not None:
        if not isinstance(column_name, str) and not isinstance(column_name, list):
            raise ValueError("coluna_cpf deve ser uma string não vazia quando fornecida.")
        cleaner.normalize_cpf(nome_coluna=column_cpf)

    if column_tel is not None:
        if not isinstance(column_tel, str) and not isinstance(column_tel, list):
            raise ValueError("column_tel deve ser uma string não vazia quando fornecida.")
        cleaner.normalize_cpf(nome_coluna=column_tel)

    return cleaner.df


def text_names_part_one_pipeline(
        df: pd.DataFrame,
        coluna_nome: str
) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Standard_text(df)

    cleaner.remover_valores_sem_letras(coluna_nome)
    cleaner.limpar_nomes_proprios(coluna_nome)

    return cleaner.df


def text_names_part_two_pipeline(
        df: pd.DataFrame,
        coluna_nome: str,
        logs_file_dir: str | Path,
) -> pd.DataFrame:
    """
    Pipeline – Parte 2 de nomes próprios:
    1. Coleta casos suspeitos
    2. Exporta fila de revisão para CSV
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Standard_text(df)

    # 1️⃣ Coleta casos suspeitos (sem mutar o DF principal)
    df_revisao = cleaner.coletar_casos_suspeitos(
        df=df,
        coluna_nome=coluna_nome
    )

    # 2️⃣ Exporta fila de revisão
    salvar_df_para_csv(df_revisao, logs_file_dir)

    return df


def text_names_part_tree_pipeline(
        df: pd.DataFrame,
        coluna_nome: str,
        path_logs: str | Path
) -> pd.DataFrame:
    """
    Pipeline – Parte 3 de nomes próprios:
    1. Lê a fila de revisão (CSV)
    2. Aplica as revisões aprovadas ao DataFrame original
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    # Se o arquivo de revisão não existir, não faz nada
    path = Path(path_logs)
    if not path.exists():
        return df

    # Lê logs de revisão
    df_logs = pd.read_csv(path, encoding="utf-8-sig")

    # Se não houver revisões, retorna df original
    if df_logs.empty:
        return df

    # Aplica revisões
    df_final = aplicar_revisao_nomes(
        df_original=df,
        df_logs=df_logs,
        coluna_nome=coluna_nome
    )

    return df_final
