from src.domain.vocabulary.temporal import *
from typing import Optional, Iterable
from datetime import date, datetime


def categorize_birth_date(
        birth_date: date | datetime | str,
        *,
        age_bins: Iterable[int],
        age_labels: Iterable[str],
) -> str:
    """
    Categorize a birth date into an age group.

    Args:
        birth_date: Date of birth (date, datetime or ISO string).
        age_bins: Upper bounds of age intervals.
        age_labels: Labels corresponding to each age interval.

    Returns:
        Age category label.

    Raises:
        ValueError: If input is invalid or age is negative.
    """
    if birth_date is None:
        raise ValueError("Birth date cannot be null.")

    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()

    elif isinstance(birth_date, str):
        try:
            birth_date = datetime.fromisoformat(birth_date).date()
        except ValueError:
            raise ValueError(f"Invalid birth date: {birth_date}")

    elif not isinstance(birth_date, date):
        raise ValueError(f"Invalid type for birth date: {type(birth_date)}")

    today = date.today()

    if birth_date > today:
        raise ValueError(f"Birth date is in the future: {birth_date}")

    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    if age < 0:
        raise ValueError(f"Invalid calculated age: {age}")

    bins = list(age_bins)
    labels = list(age_labels)

    if len(labels) != len(bins) - 1:
        raise ValueError("age_labels must have len(age_bins) - 1 elements.")

    for i in range(len(bins) - 1):
        lower = bins[i]
        upper = bins[i + 1]
        if lower <= age <= upper:
            return labels[i]

    raise ValueError(f"Age {age} does not fit in provided bins.")


def classify_year_interval(value: int | str | date | datetime) -> Optional[str]:
    """
    Classify a year (or year-bearing value) into a predefined semantic interval.

    Supported inputs:
        - int year
        - date/datetime (uses .year)
        - str in formats: YYYY-MM-DD, DD/MM/YYYY, YYYY

    Classification rule:
        Uses (start, end] intervals: start < year <= end.

    Args:
        value: Input value containing a year.

    Returns:
        Interval label if the year fits a bin; otherwise None.
    """
    year: Optional[int] = None

    if isinstance(value, int):
        year = value
    elif isinstance(value, (date, datetime)):
        year = value.year
    elif isinstance(value, str):
        text = value.strip()
        if text:
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y"):
                try:
                    year = datetime.strptime(text, fmt).year
                    break
                except ValueError:
                    continue

    if year is None or year < 0:
        return None

    if len(YEAR_RANGE_LABELS) != len(YEAR_BINS) - 1:
        raise ValueError("YEAR_RANGE_LABELS must have len(YEAR_BINS) - 1 elements.")

    for i in range(len(YEAR_BINS) - 1):
        start = YEAR_BINS[i]
        end = YEAR_BINS[i + 1]

        if start < year <= end:
            return YEAR_RANGE_LABELS[i]

    return None