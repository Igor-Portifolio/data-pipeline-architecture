import geopandas as gpd
import pandas as pd


def ler_arquivo_gpkg(path: str) -> pd.DataFrame:
    """
    Lê um arquivo GeoPackage (.gpkg) e retorna um DataFrame.
    """

    if not isinstance(path, str):
        raise ValueError("O caminho do arquivo deve ser uma string.")

    try:
        gdf = gpd.read_file(path)
    except Exception as e:
        raise IOError(f"Erro ao ler arquivo gpkg: {e}")

    # Converte para DataFrame comum se geometria não for necessária
    df = pd.DataFrame(gdf)

    return df
