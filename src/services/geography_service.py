import pandas as pd
from src.domain.rules.geography import classify_state_region

class StateRegionClassificationService:
    """
    Service responsible for applying state-to-region classification
    to a pandas DataFrame.

    This service delegates the classification logic to the
    domain layer and applies it to one or more DataFrame columns.

    It performs structural transformations only and does not
    implement additional business rules.

    Args:
        df: Input DataFrame to be processed. A copy is stored internally.
    """

    def __init__(self, df: pd.DataFrame, ):
        self.df = df.copy()

    def add_region_column(self, column: str) -> pd.DataFrame:
        """
        Add a region column next to the specified state column,
        classifying each value using the domain-level region classifier.

        Args:
            column: Name of the column containing state values.

        Returns:
            The updated DataFrame with the region column inserted
            immediately after the specified column.

        Raises:
            KeyError: If the specified column does not exist.
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' not found in DataFrame.")

        regions = self.df[column].apply(classify_state_region)

        idx = self.df.columns.get_loc(column) + 1

        self.df.insert(idx, "region", regions)

        return self.df