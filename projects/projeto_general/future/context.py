from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import pandas as pd

from projects.projeto_general.future.config import ClientConfig


@dataclass(frozen=True)
class ProjectContext:
    """
    Contexto imutável da execução:
    - config: parâmetros do cliente (colunas, tipo, etc.)
    - paths: dicionário de paths produzido por build_paths()
        chaves esperadas: input, staging, logs, curated, final_name, revision
    """
    config: ClientConfig
    paths: Dict[str, Any]


@dataclass
class StepState:
    """
    Estado mutável carregado ao longo do pipeline.
    Começa vazio e vai sendo preenchido.
    """
    df: Optional[pd.DataFrame] = None
