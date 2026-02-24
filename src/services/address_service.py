import pandas as pd
from src.domain.rules.address import address_domain_pipeline, district_domain_pipeline


class AddressNormalizationService:
    """
    Service responsible for applying address normalization rules
    to a pandas DataFrame.

    This service delegates domain-level normalization logic to the
    address domain module and applies it to one or more DataFrame
    columns.

    It performs structural transformations only and does not
    implement business rules beyond address normalization.

    Args:
        df: Input DataFrame to be processed. A copy is stored internally.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def normalize_address_column(self, column: str) -> pd.DataFrame:
        """
        Apply address normalization to a specific DataFrame column,
        overwriting the original values.

        Args:
            column: Name of the column to normalize.

        Returns:
            The updated DataFrame with normalized address values.

        Raises:
            KeyError: If the specified column does not exist.
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' not found in DataFrame.")

        self.df[column] = self.df[column].apply(address_domain_pipeline)

        return self.df

    def normalize_district_column(self, column: str) -> pd.DataFrame:
        """
        Apply district normalization to a specific DataFrame column,
        overwriting the original values.

        Args:
            column: Name of the column to normalize.

        Returns:
            The updated DataFrame with normalized district values.

        Raises:
            KeyError: If the specified column does not exist.
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' not found in DataFrame.")

        self.df[column] = self.df[column].apply(district_domain_pipeline)

        return self.df

    def split_districts_by_state(
            self,
            district_column: str,
            state_column: str,
    ) -> dict[str, pd.DataFrame]:
        """
        Split the DataFrame into multiple DataFrames by state while preserving
        traceability for manual review.

        The output for each state includes:
          - original row index (`row_id`)
          - state value
          - original district value
          - an empty field for normalized district
          - a review flag placeholder
          - an approval flag defaulting to True

        Args:
            district_column: Name of the column containing district values.
            state_column: Name of the column containing state values.

        Returns:
            A dictionary mapping each state (as string) to a review DataFrame.

        Raises:
            KeyError: If either column does not exist.
        """
        if district_column not in self.df.columns:
            raise KeyError(f"Column '{district_column}' not found in DataFrame.")

        if state_column not in self.df.columns:
            raise KeyError(f"Column '{state_column}' not found in DataFrame.")

        result: dict[str, pd.DataFrame] = {}

        df_base = self.df.copy()

        for state, df_state in df_base.groupby(state_column):
            df_out = pd.DataFrame(
                {
                    "row_id": df_state.index,
                    "state": state,
                    "district_original": df_state[district_column].values,
                    "district_normalized": [""] * len(df_state),
                    "requires_review": [pd.NA] * len(df_state),
                    "approved": [True] * len(df_state),
                }
            )

            result[str(state)] = df_out.reset_index(drop=True)

        return result
