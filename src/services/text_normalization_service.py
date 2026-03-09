from typing import Optional, Union, List
from src.domain.rules.name_normalization import clean_name_domain_pipeline
import pandas as pd
from src.domain.vocabulary.language import tel_len, preposicoes_minusculas
from typing import Iterable
from src.domain.primitives.text_normalization import remove_accents, smart_titlecase, normalize_person_name_characters
from src.domain.rules.string_matching import is_valid_email


class TextNormalizationService:
    """
    Service responsible for applying text normalization rules to a DataFrame.

    This class operates at the service layer and coordinates transformations
    over one or more text columns using domain and primitive functions.

    Characteristics:
        - Works on a copy of the provided DataFrame.
        - Does not mutate the original DataFrame.
        - Orchestrates transformations but does not define business rules.

    Args:
        df: Input pandas DataFrame to be processed.

    Attributes:
        df: Internal working copy of the DataFrame.
    """

    def __init__(self, df: pd.DataFrame, ):
        self.df = df.copy()

    def _get_string_columns(self) -> list:
        return list(self.df.select_dtypes(include=["object", "string"]).columns)

    def normalize_text(
            self,
            columns: Optional[Union[str, List[str]]] = None,
            *,
            upper: bool = False,
            lower: bool = False,
            name: bool = False,
            remove_diacritics: bool = False,
    ) -> pd.DataFrame:
        """
        Normalize text columns in the DataFrame.

        Rules:
            - Always trims surrounding whitespace.
            - Applies only one casing rule in order:
              upper > lower > name > none.
            - Optionally removes diacritics.
            - Preserves missing values (pd.NA).

        Args:
            columns: Column name or list of column names.
                If None, all object/string columns are processed.
            upper: Convert text to uppercase.
            lower: Convert text to lowercase.
            name: Apply smart title case.
            remove_diacritics: Remove accents.

        Returns:
            DataFrame with normalized text.
        """
        if columns is None:
            cols_to_process = self.df.select_dtypes(include=["object", "string"]).columns
        else:
            cols_to_process = [columns] if isinstance(columns, str) else columns

        for col in cols_to_process:
            if col not in self.df.columns:
                continue

            series = self.df[col].astype("string").str.strip()

            if upper:
                new_series = series.str.upper()
            elif lower:
                new_series = series.str.lower()
            elif name:
                new_series = series.map(
                    lambda x: x if pd.isna(x) else smart_titlecase(x, lowercase_words=preposicoes_minusculas)
                )
            else:
                new_series = series

            if remove_diacritics:
                new_series = new_series.map(
                    lambda x: x if pd.isna(x) else remove_accents(x)
                )

            self.df[col] = new_series

        return self.df

    def clean_proper_names_column(self,
                                  column: str,
                                  *,
                                  keep_numbers: bool = False,
                                  keep_professions: bool = False,
                                  keep_political: bool = False,
                                  keep_universities: bool = False,
                                  keep_states: bool = False,
                                  ) -> pd.DataFrame:
        """
        Apply the proper-name cleaning domain pipeline to a DataFrame column.

        Args:
            column: Name of the column to process.
            keep_numbers: If True, skips character normalization that would remove digits.
            keep_professions: If True, skips character normalization that would remove professions.
            keep_political: If True, skips character normalization that would remove political parties.
            keep_universities: If True, skips character normalization that would remove universities.
            keep_states: If True, skips character normalization that would remove states.
        Returns:
            DataFrame with the cleaned column.
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' was not found in the DataFrame.")

        self.df[column] = self.df[column].apply(
            lambda x: clean_name_domain_pipeline(x,
                                                 keep_numbers=keep_numbers,
                                                 keep_states= keep_states,
                                                 keep_universities= keep_universities,
                                                 keep_political=keep_political,
                                                 keep_professions=keep_professions
                                                ))

        return self.df

    def remove_values_without_letters(self, column: str) -> pd.DataFrame:
        """
        Set values to pd.NA when, after name character normalization,
        the result contains no remaining characters.

        Args:
            column: Name of the column to process.

        Returns:
            DataFrame with values without letters removed (set to pd.NA).
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' was not found in the DataFrame.")

        self.df[column] = self.df[column].apply(
            lambda value: pd.NA
            if isinstance(value, str) and normalize_person_name_characters(value) == ""
            else value
        )

        return self.df

    def normalize_phone_column(
            self,
            column: str,
            *,
            allowed_lengths: Iterable[int] = tel_len,
    ) -> pd.DataFrame:
        """
        Normalize phone numbers in a DataFrame column.

        Rules:
            - Converts values to pandas string dtype and trims whitespace.
            - Keeps digits only.
            - Sets empty results to pd.NA.
            - Validates length against `allowed_lengths`.
            - Keeps only valid digit strings; invalid values become pd.NA.

        Args:
            column: Column name containing phone-like values.
            allowed_lengths: Allowed digit counts for a phone number.

        Returns:
            DataFrame with the normalized phone column.
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' was not found in the DataFrame.")

        out = self.df.copy()

        series = out[column].astype("string").str.strip()
        digits = series.str.replace(r"\D", "", regex=True).replace("", pd.NA)

        valid_lengths = set(allowed_lengths)
        valid_mask = digits.notna() & digits.str.len().isin(valid_lengths)

        out[column] = digits.mask(~valid_mask, pd.NA)

        self.df = out
        return self.df

    def normalize_cpf_column(
            self,
            column: str,
            *,
            cpf_length: int = 11,
    ) -> pd.DataFrame:
        """
        Normalize CPF values in a DataFrame column.

        Rules:
            - Converts values to pandas string dtype and trims whitespace.
            - Keeps digits only.
            - Sets empty results to pd.NA.
            - Validates exact length (`cpf_length`).
            - Keeps only valid digit strings; invalid values become pd.NA.

        Args:
            column: Column name containing CPF-like values.
            cpf_length: Required number of digits for a valid CPF.

        Returns:
            DataFrame with the normalized CPF column.
        """
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' was not found in the DataFrame.")

        out = self.df.copy()

        series = out[column].astype("string").str.strip()
        digits = series.str.replace(r"\D", "", regex=True).replace("", pd.NA)

        valid_mask = digits.notna() & (digits.str.len() == cpf_length)

        out[column] = digits.mask(~valid_mask, pd.NA)

        self.df = out
        return self.df

    def validate_email_column(
            self,
            column: str,
    ) -> pd.DataFrame:
        """
        Validate email values in a specific column.

        Invalid email values are replaced with pd.NA.
        Valid email values remain unchanged.

        Args:
            column: Name of the column containing email values.

        Returns:
            A DataFrame with invalid emails removed (set to pd.NA).

        Raises:
            KeyError: If the specified column does not exist.
        """

        df = self.df.copy()

        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found in DataFrame.")

        def validate(value):
            if is_valid_email(value):
                return value
            return pd.NA

        df[column] = df[column].apply(validate)

        self.df = df
        return df

    def move_email_from_name_column(
            self,
            column_name: str,
            column_email: str,
    ) -> pd.DataFrame:
        """
        Move valid email values from a name column to an email column when needed.

        For each row:
            - If `column_name` contains a valid email:
                - If `column_email` is empty, move the value to `column_email`
                  and set `column_name` to pd.NA.
                - If `column_email` is already filled, do nothing.
            - If `column_name` does not contain a valid email, do nothing.

        Args:
            column_name: Column that may contain misplaced email values.
            column_email: Target email column.

        Returns:
            A DataFrame with corrected email placement.

        Raises:
            KeyError: If either column does not exist.
        """

        df = self.df.copy()

        if column_name not in df.columns:
            raise KeyError(f"Column '{column_name}' not found in DataFrame.")

        if column_email not in df.columns:
            raise KeyError(f"Column '{column_email}' not found in DataFrame.")

        name_series = df[column_name]
        email_series = df[column_email]

        name_as_str = name_series.astype("string").str.strip()
        name_has_email = name_as_str.map(is_valid_email)

        email_as_str = email_series.astype("string").str.strip()
        email_is_empty = email_as_str.isna() | (email_as_str == "")

        should_move = name_has_email & email_is_empty

        df.loc[should_move, column_email] = name_series.loc[should_move]
        df.loc[should_move, column_name] = pd.NA

        self.df = df
        return df
