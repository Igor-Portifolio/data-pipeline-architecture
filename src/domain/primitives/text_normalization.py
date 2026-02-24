import re
from unidecode import unidecode
from src.domain.vocabulary.voc_lingua import preposicoes_minusculas
from typing import Iterable


def normalize_person_name_characters(text: str) -> str:
    """
    Normalize characters for person-name-like text.

    Rules:
        - Keeps only Latin letters (including accents), spaces and apostrophes.
        - Removes leading and trailing apostrophes.
        - Removes isolated apostrophes between spaces.
        - Normalizes consecutive whitespace into a single space.

    Args:
        text: Input string to normalize.

    Returns:
        Cleaned string. Returns empty string if input is not a string.
    """
    if not isinstance(text, str):
        return ""

    text = re.sub(r"[^A-Za-zÀ-ÿ\s']", "", text)
    text = re.sub(r"^'+", "", text)
    text = re.sub(r"'+$", "", text)
    text = re.sub(r"\s+'\s+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def remove_accents(text: str) -> str:
    """
    Remove diacritical marks from text using transliteration.

    Args:
        text: Input string to process.

    Returns:
        Text without accents. Returns empty string if input is not a string.
    """
    if not isinstance(text, str):
        return ""

    return unidecode(text)



def smart_titlecase(
    text: str,
    *,
    lowercase_words: Iterable[str] = preposicoes_minusculas,
) -> str:
    """
    Apply intelligent title casing to text.

    Words listed in `lowercase_words` remain lowercase
    unless they are the first word in the string.

    Args:
        text: Input string to transform.
        lowercase_words: Iterable of words that should remain lowercase
            when not in first position.

    Returns:
        Title-cased string. Returns empty string if input is not a string
        or is empty.
    """
    if not isinstance(text, str):
        return ""

    text = text.strip()
    if not text:
        return ""

    words = text.split()
    result: list[str] = []

    lowercase_set = {w.lower() for w in lowercase_words}

    for index, word in enumerate(words):
        word_lower = word.lower()

        if index != 0 and word_lower in lowercase_set:
            result.append(word_lower)
        else:
            result.append(word_lower.capitalize())

    return " ".join(result)
