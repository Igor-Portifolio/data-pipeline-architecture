from src.services.geography_service import StateRegionClassificationService
import pandas as pd

def geography_pipeline(
    df: pd.DataFrame,
    state_column: str,
) -> pd.DataFrame:
    """
    Executes the geographic pipeline.

    Classifies states into regions.

    Args:
        df (pd.DataFrame): Input DataFrame.
        state_column (str): Column containing state values.

    Returns:
        pd.DataFrame: DataFrame with region classification applied.

    Raises:
        TypeError: If df is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    classifier = StateRegionClassificationService(df)
    classifier.add_region_column(state_column)

    return classifier.df
