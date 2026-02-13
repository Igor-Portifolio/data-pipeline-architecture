from src.services.geral_subjects.texto import *
from src.infra.io.writers import *
from src.infra.io.paths import *


def text_basic_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Standard_text(df)

    # 1️⃣ Remove emojis, pictogramas e símbolos
    cleaner.remover_emojis_e_simbolos()

    # 2️⃣ Normalização padrão do pipeline
    cleaner.normalize_text(
        upper=True,
        remover_acentos=True
    )

    return cleaner.df


def text_names_part_one_pipeline(
        df: pd.DataFrame,
        coluna: str
) -> pd.DataFrame:
    """
    Pipeline – Parte 1 de limpeza de nomes próprios:
    1. Remove valores sem letras
    2. Aplica limpeza semântica de nomes próprios
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    cleaner = Standard_text(df)

    # 1️⃣ Remove valores que não contêm letras
    cleaner.remover_valores_sem_letras(coluna)

    # 2️⃣ Limpeza semântica de nomes próprios
    cleaner.limpar_nomes_proprios(coluna)

    return cleaner.df


def text_names_part_two_pipeline(
        df: pd.DataFrame,
        coluna: str,
        path_saida: str
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
        coluna_nome=coluna
    )

    # 2️⃣ Exporta fila de revisão
    salvar_df_para_csv(df, logs_dir)

    return df


def text_names_part_tree_pipeline(
        df: pd.DataFrame,
        coluna: str,
        path_saida: str
) -> pd.DataFrame:
    """
    Pipeline – Parte 3 de nomes próprios:
    1. Lê a fila de revisão (CSV)
    2. Aplica as revisões aprovadas ao DataFrame original
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Entrada deve ser um pandas DataFrame")

    # Se o arquivo de revisão não existir, não faz nada
    path = Path(path_saida)
    if not path.exists():
        return df

    # Lê logs de revisão
    df_logs = pd.read_csv(path, encoding="utf-8-sig")

    # Se não houver revisões, retorna df original
    if df_logs.empty:
        return df

    # Aplica revisões
    df_final = aplicar_revisao_manual(
        df_original=df,
        df_revisao=df_logs,
        nome_coluna_df=coluna
    )

    return df_final
