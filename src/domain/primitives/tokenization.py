import re
from typing import List


def tokenize_words(
    text: str,
    *,
    to_lower: bool = False,
    to_upper: bool = False,
) -> List[str]:
    """
    Split a text string into whitespace-delimited tokens.

    This function performs minimal structural normalization:
    - Strips leading and trailing whitespace
    - Collapses multiple internal spaces
    - Splits by whitespace

    It does not remove punctuation or apply domain-specific rules.

    Args:
        text: Input string to tokenize.
        to_lower: If True, convert text to lowercase before tokenization.
        to_upper: If True, convert text to uppercase before tokenization.

    Returns:
        A list of tokens extracted from the input string.
        Returns an empty list if input is invalid or blank.

    Raises:
        ValueError: If both `to_lower` and `to_upper` are True.
    """
    if not isinstance(text, str):
        return []

    if to_lower and to_upper:
        raise ValueError("Cannot set both 'to_lower' and 'to_upper' to True.")

    text = text.strip()
    if not text:
        return []

    if to_lower:
        text = text.lower()
    elif to_upper:
        text = text.upper()

    text = re.sub(r"\s+", " ", text)

    return text.split(" ")