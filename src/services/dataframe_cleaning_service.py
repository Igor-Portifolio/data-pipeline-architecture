from src.domain.primitives.series_ops import safe_replace
from src.domain.primitives.value_coersion import coerce_value
from src.domain.primitives.text_normalization import trim_whitespace_value
import pandas as pd


class DataFrameSanitizationService:
    """
    Service responsible for structural sanitization of a pandas DataFrame.

    This service performs non-semantic, deterministic transformations such as:
        - Null normalization
        - Exact duplicate removal
        - Type coercion
        - Whitespace trimming
        - Text punctuation normalization
        - Date formatting

    Architectural role:
        - Operates at the service layer
        - Orchestrates DataFrame-level transformations
        - Does not implement business/domain rules
        - May depend on primitive or domain functions
        - Mutates internal state (self.df) in a controlled manner

    Guarantees:
        - No business logic is introduced
        - Only structural cleaning operations are applied
        - Raises explicit errors for invalid column references

    This class is intended to be used as an imperative shell
    around a functional domain core.
    """

    def __init__(self, df: pd.DataFrame, ):
        self.df = df.copy()

    def normalize_nulls(
            self,
            coluna: str | None = None,
            nulo: str | None = None,
    ) -> pd.DataFrame:
        """
        Normalize null-like values in a specific column or across the entire DataFrame.

        Args:
            coluna: Column name to apply normalization. If None, applies to all columns.
            nulo: If None, null-like values are converted to pd.NA.
                  If provided, null-like values are replaced with the given string.

        Returns:
            A DataFrame with normalized null values.

        Raises:
            KeyError: If the specified column does not exist.
        """

        df = self.df.copy()

        null_tokens: list[str] = [
            "",
            " ",
            "nan",
            "None",
            "not_available",
            "<NA>",
            "NAN",
            "Nan",
            "<na>",
        ]

        def substituir(serie: pd.Series) -> pd.Series:
            if nulo is None:
                return safe_replace(serie, null_tokens, pd.NA)

            tokens_with_na = ["", " ", "nan", "None", pd.NA]
            return safe_replace(serie, tokens_with_na, nulo)

        if coluna is None:
            for col in df.columns:
                df[col] = substituir(df[col])
        else:
            if coluna not in df.columns:
                raise KeyError(f"Column '{coluna}' not found in DataFrame.")
            df[coluna] = substituir(df[coluna])

        self.df = df
        return df

    def drop_exact_duplicates(
            self,
            coluna: str | None = None,
    ) -> pd.DataFrame:
        """
        Remove exact duplicate rows from the DataFrame.

        Args:
            coluna: Column name to evaluate duplicates. If None, the entire row
                    must be identical to be considered duplicate.

        Returns:
            A DataFrame with duplicate rows removed.

        Raises:
            KeyError: If the specified column does not exist.
        """

        df = self.df.copy()

        if coluna is None:
            df = df.drop_duplicates(ignore_index=True)
        else:
            if coluna not in df.columns:
                raise KeyError(f"Column '{coluna}' not found in DataFrame.")
            df = df.drop_duplicates(subset=[coluna], ignore_index=True)

        self.df = df.copy()
        return self.df

    def coerce_types(
            self,
            coluna: str | None = None,
    ) -> pd.DataFrame:
        """
        Coerce values to inferred Python types in one column or across the entire DataFrame.

        Args:
            coluna: Column name to coerce. If None, applies to all columns.

        Returns:
            A DataFrame with coerced values.

        Raises:
            KeyError: If the specified column does not exist.
        """

        df = self.df.copy()

        if coluna is None:
            for col in df.columns:
                df[col] = df[col].apply(coerce_value)
        else:
            if coluna not in df.columns:
                raise KeyError(f"Column '{coluna}' not found in DataFrame.")
            df[coluna] = df[coluna].apply(coerce_value)

        self.df = df
        return df

    def trim_whitespace(self) -> pd.DataFrame:
        """
        Remove leading, trailing, invisible, and redundant whitespace
        across the entire DataFrame.

        Returns:
            A DataFrame with whitespace-normalized values.
        """

        df = self.df.copy()

        for col in df.columns:
            df[col] = df[col].apply(trim_whitespace_value)

        self.df = df
        return df

    # def normalizar_pontuacao(
    #         self,
    #         coluna: str | None = None
    # ) -> pd.DataFrame:
    #     """
    #     Aplica a normalização de pontuação em uma coluna específica
    #     ou em todo o DataFrame.
    #     """
    #
    #     def aplicar(valor):
    #         if isinstance(valor, str):
    #             return normalizar_pontuacao_texto(valor)
    #         return valor
    #
    #     if coluna:
    #         if coluna not in self.df.columns:
    #             raise KeyError(f"Coluna '{coluna}' não encontrada.")
    #
    #         self.df[coluna] = self.df[coluna].apply(aplicar)
    #
    #     else:
    #         for col in self.df.columns:
    #             self.df[col] = self.df[col].apply(aplicar)
    #
    #     return self.df

    def format_date_column_ddmmyyyy(
            self,
            coluna_data: str,
    ) -> pd.DataFrame:
        """
        Convert a date column to the format 'dd/mm/yyyy' (no time component).

        Args:
            coluna_data: Name of the column to be formatted.

        Returns:
            A DataFrame with the formatted date column.

        Raises:
            KeyError: If the specified column does not exist.
            ValueError: If the column cannot be converted to datetime.
        """

        df = self.df.copy()

        if coluna_data not in df.columns:
            raise KeyError(f"Column '{coluna_data}' not found in DataFrame.")

        try:
            df[coluna_data] = (
                pd.to_datetime(df[coluna_data], errors="raise")
                .dt.strftime("%d/%m/%Y")
            )
        except Exception as exc:
            raise ValueError(
                f"Failed to convert column '{coluna_data}' to datetime: {exc}"
            )

        self.df = df
        return df
