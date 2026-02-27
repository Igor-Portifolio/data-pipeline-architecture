import geopandas as gpd
from pathlib import Path
import pandas as pd


dir = Path(__file__).parent.parent.parent
arquivo_path = dir / "data" / "raw" / "ref" /"BR_bairros_CD2022.gpkg"

# Ler o arquivo
gdf = gpd.read_file(arquivo_path)

# Converter GeoDataFrame para DataFrame do pandas (sem geometria)
df = pd.DataFrame(gdf.drop(columns=['geometry']))

pass