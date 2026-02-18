from __future__ import annotations

from projects.projeto_geral.context import ProjectContext, StepState

from src.pipelines.auto.basic_pipeline import basic_pipeline_1st, basic_pipeline_2st
from src.pipelines.auto.text_pipeline import (
    text_basic_pipeline,
    text_names_part_one_pipeline,
    text_names_part_two_pipeline,
    text_names_part_tree_pipeline
)


def run(ctx: ProjectContext, state: StepState) -> StepState:
    if state.df is None:
        raise RuntimeError("transform: df não carregado. Rode ingest antes.")

    df = state.df
    cfg = ctx.config
    paths = ctx.paths

    # 1) Basic (data)
    if cfg.date_column:
        df = basic_pipeline_1st(df, coluna_data=cfg.date_column)

    # 2) Text basic
    df = text_basic_pipeline(
        df,
        columns_strings=cfg.string_columns,
        column_email=cfg.email_column,
        column_name=cfg.name_column,
        column_cpf=cfg.cpf_column,
        column_tel=cfg.phone_column,
    )

    # 3) Nomes em 2 fases (com revisão manual entre elas)
    # names_mode:
    #   - "stage1": roda só part_one (pré-revisão)
    #   - "stage2": roda só part_tree (pós-revisão, usando logs)
    #   - "all": roda ambos (não recomendado para seu fluxo manual)
    names_mode = paths.get("names_mode", "stage1")  # default seguro pro seu caso

    if cfg.name_column:
        logs_path = paths["logs"]

        if names_mode == "stage1":
            df = text_names_part_one_pipeline(df, cfg.name_column)
            print("[TRANSFORM] names_mode=stage1 -> gerado pré-processamento de nomes. Faça revisão manual e rode stage2.")
        elif names_mode == "stage2":
            df = text_names_part_two_pipeline(df, coluna_nome=cfg.name_column, path_logs=logs_path)
            print("[TRANSFORM] names_mode=stage2 -> aplicado pós-revisão de nomes a partir do log.")
        elif names_mode == "stage3":
            df = text_names_part_tree_pipeline(df, coluna_nome=cfg.name_column, path_logs=logs_path)
            print("[TRANSFORM] names_mode=stage3 -> Limpeza final aplicada de nomes com log manual.")
        else:
            raise ValueError(f"names_mode inválido: {names_mode}. Use stage1, stage2 ou stage3.")
    else:
        print("[TRANSFORM] name_column=None -> pulando limpeza de nomes.")

    # 4) Final null handling
    df = basic_pipeline_2st(df)

    state.df = df
    return state
