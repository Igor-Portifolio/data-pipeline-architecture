from src.domain.vocabulary.voc_lingua import DOMINIOS_EMAIL_COMUNS
from src.domain.rules.name_normalization import evaluate_name_flags
from typing import Any
import pandas as pd


def collect_suspicious_name_cases(
        df: pd.DataFrame,
        name_column: str,
) -> pd.DataFrame:
    """
    Analyze a name-like column and return a review report
    for records flagged by domain validation rules.

    If an email-domain flag is detected, the function attempts
    to automatically remove known email domain patterns
    from the original value.

    Args:
        df: Input DataFrame to analyze.
        name_column: Column containing name-like values.

    Returns:
        DataFrame with:
            - record_id
            - original_value
            - reasons
            - applied_rules
            - revised_value
    """
    if name_column not in df.columns:
        raise KeyError(f"Column '{name_column}' was not found in the DataFrame.")

    records: list[dict[str, Any]] = []

    for idx, value in df[name_column].items():
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
