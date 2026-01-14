from src.services.ibge_service import *
from pathlib import Path

dir = Path(__file__).parent.parent.parent
arquivo_path_gpkg = dir / "data" / "raw" / "ref" /"BR_bairros_CD2022.gpkg"
db_path  = dir / "data" / "store" / "memory.db"

ingestao_ibge_sqlite(arquivo_path_gpkg, db_path, "IBGE")

