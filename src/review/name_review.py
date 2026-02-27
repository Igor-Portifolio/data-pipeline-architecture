from src.domain.vocabulary.language import DOMINIOS_EMAIL_COMUNS
from src.domain.rules.name_normalization import evaluate_name_flags
from typing import Any
import pandas as pd


def collect_suspicious_name_cases(
        df: pd.DataFrame,
        column: str,
) -> pd.DataFrame:
    """
    Analyze a name-like column and return a review report
    for records flagged by domain validation rules.

    If an email-domain flag is detected, the function attempts
    to automatically remove known email domain patterns
    from the original value.

    Args:
        df: Input DataFrame to analyze.
        column: Column containing name-like values.

    Returns:
        DataFrame with:
            - record_id
            - original_value
            - reasons
            - applied_rules
            - revised_value
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' was not found in the DataFrame.")

    records: list[dict[str, Any]] = []

    for idx, value in df[column].items():
        if not isinstance(value, str):
            continue

        reasons = evaluate_name_flags(value)
        if not reasons:
            continue

        revised_value = value

        if "EMAIL" in reasons:
            value_lower = value.lower()

            for domain in DOMINIOS_EMAIL_COMUNS:
                domain_lower = domain.lower()
                variants = (domain_lower, domain_lower.replace(".", ""))

                for variant in variants:
                    pos = value_lower.find(variant)
                    if pos != -1:
                        revised_value = value[:pos]
                        break

                if revised_value != value:
                    break

        revised_value = revised_value.strip()

        records.append(
            {
                "record_id": idx,
                "original_value": value,
                "reasons": reasons,
                "applied_rules": list(reasons),
                "revised_value": revised_value,
            }
        )

    return pd.DataFrame(
        records,
        columns=[
            "record_id",
            "original_value",
            "reasons",
            "applied_rules",
            "revised_value",
        ],
    )


import pandas as pd


def apply_name_review(
    df_original: pd.DataFrame,
    df_logs: pd.DataFrame,
    column_name: str,
) -> pd.DataFrame:
    """
    Applies name revisions to the original DataFrame based on a review log.

    Updates values only when `valor_revisado` is valid (non-empty string).

    Args:
        df_original (pd.DataFrame): Original DataFrame to be updated.
        df_logs (pd.DataFrame): DataFrame containing revision logs.
        column_name (str): Column name in df_original to be updated.

    Returns:
        pd.DataFrame: A copy of df_original with revisions applied.

    Raises:
        TypeError: If df_original or df_logs is not a DataFrame.
        KeyError: If required columns are missing.
    """
    if not isinstance(df_original, pd.DataFrame):
        raise TypeError("df_original must be a DataFrame")

    if not isinstance(df_logs, pd.DataFrame):
        raise TypeError("df_logs must be a DataFrame")

    if column_name not in df_original.columns:
        raise KeyError(f"Column '{column_name}' not found in df_original")

    for col in ["record_id", "revised_value"]:
        if col not in df_logs.columns:
            raise KeyError(f"Column '{col}' not found in df_logs")

    df_final = df_original.copy()

    for _, row in df_logs.iterrows():
        idx = row["record_id"]
        revised_value = row["revised_value"]

        if idx not in df_final.index:
            continue

        if not isinstance(revised_value, str):
            df_final.at[idx, column_name] = pd.NA
            continue

        cleaned_value = revised_value.strip()

        if cleaned_value == "":
            df_final.at[idx, column_name] = pd.NA
        else:
            df_final.at[idx, column_name] = cleaned_value

    return df_final
