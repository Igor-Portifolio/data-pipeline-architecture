"""
projects/projeto_geral/run.py

Runner simples com:
- pipelines como listas de steps (p1, p2, full)
- flags: --pipeline, --revision
- opcional: --until para parar em um step

Exemplos:
  python -m projects.projeto_geral.run --pipeline p1 --revision RevA
  python -m projects.projeto_geral.run --pipeline full --revision RevB --until transform
"""

from __future__ import annotations

import argparse
from typing import Callable, Iterable, Optional, Tuple

from projects.projeto_geral.config import config  # instancia de ClientConfig
from projects.projeto_geral.paths import build_paths
from projects.projeto_geral.context import ProjectContext, StepState

from projects.projeto_geral.steps import ingest, transform, quality_report, export


StepFn = Callable[[ProjectContext, StepState], StepState]
Step = Tuple[str, StepFn]


PIPELINES: dict[str, list[Step]] = {
    "p1": [
        ("ingest", ingest.run),
        ("transform", transform.run),
    ],
    "p2": [
        ("quality_report", quality_report.run),
        ("export", export.run),
    ],
    "full": [
        ("ingest", ingest.run),
        ("transform", transform.run),
        ("quality_report", quality_report.run),
        ("export", export.run),
    ],
}


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Runner do projeto_geral")
    parser.add_argument(
        "--pipeline",
        choices=PIPELINES.keys(),
        default="full",
        help="Qual pipeline rodar: p1, p2 ou full",
    )
    parser.add_argument(
        "--revision",
        default="RevA",
        help="Revisão do output (ex: RevA, RevB). Default: RevA",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="(Opcional) Para após executar este step. Ex: --until transform",
    )
    parser.add_argument(
        "--names-mode",
        choices=["stage1", "stage2", "stage3"],
        default="stage1",
        help="Modo de execução da limpeza de nomes",
    )
    return parser.parse_args(argv)


def run_steps(steps: Iterable[Step], ctx: ProjectContext, *, until: Optional[str] = None) -> StepState:
    # valida cedo se --until existe no pipeline escolhido
    if until is not None:
        step_names = [name for name, _ in steps]
        if until not in step_names:
            raise ValueError(f"--until='{until}' não existe nesse pipeline. Steps: {step_names}")

    state = StepState()

    for step_name, step_fn in steps:
        print(f"[RUN] {step_name}")
        state = step_fn(ctx, state)

        if until is not None and step_name == until:
            print(f"[STOP] Parando em --until {until}")
            break

    return state


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    # monta contexto (imutável)
    paths = build_paths(config, revision=args.revision)
    paths["names_mode"] = args.names_mode
    ctx = ProjectContext(config=config, paths=paths)

    # escolhe pipeline
    steps = PIPELINES[args.pipeline]

    # executa
    run_steps(steps, ctx, until=args.until)

    print(f"[DONE] pipeline={args.pipeline} revision={args.revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
