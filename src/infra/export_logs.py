import pandas as pd
from pathlib import Path


def exportar_fila_revisao_nomes(
    df_revisao: pd.DataFrame,
    path_saida: str,
    formato: str = "csv",
) -> str:
    """
    Exporta a fila de revisão de nomes para inspeção humana.

    Responsabilidade:
    - Apenas escrever o DataFrame em disco
    - Sobrescreve o arquivo se já existir
    """

    if formato.lower() != "csv":
        raise ValueError("Formato não suportado. Use apenas 'csv'.")

    path = Path(path_saida)

    df_revisao.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",  # importante para Excel
    )

    return str(path)


def create_feedback_file(rev: str) -> Path:
    """
    Cria a pasta 'text_files' ao lado da pasta src.
    Gera um arquivo client_feedback_<rev>.txt.
    Se já existir, sobrescreve.
    """

    # Caminho absoluto deste arquivo
    current_file = Path(__file__).resolve()

    # Raiz do projeto (pasta pai da src)
    project_root = current_file.parent.parent

    # Pasta de saída
    folder = project_root / "text_files"
    folder.mkdir(exist_ok=True)

    # Nome baseado na revisão
    file_name = f"client_feedback_{rev}.txt"
    file_path = folder / file_name

    # Cria ou sobrescreve
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{rev}:\n\n")

    return file_path
