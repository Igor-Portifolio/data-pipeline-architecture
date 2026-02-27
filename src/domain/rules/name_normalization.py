from src.domain.vocabulary.language import *
import re
from typing import List, Optional
from src.domain.primitives.tokenization import tokenize_words
from src.domain.primitives.text_normalization import normalize_person_name_characters


def flag_long_name(text: str, *, min_length: int = 12) -> str | None:
    """
    Flag text if any token exceeds a given length threshold.

    Args:
        text: Input string to evaluate.
        min_length: Minimum token length required to trigger the flag.

    Returns:
        "((LONG_NAME))" if any token length is greater than or equal
        to the threshold, otherwise None.
    """
    tokens = tokenize_words(text)

    if any(len(token) >= min_length for token in tokens):
        return "LONG_NAME"

    return None


def flag_email(text: str) -> str | None:
    """
    Flag text if it contains a known email domain pattern,
    even if the domain appears without punctuation or with spaces.

    Examples detected:
        - user@gmail.com
        - user gmail com
        - user gmailcom
        - user gmail com br

    Args:
        text: Input string to evaluate.

    Returns:
        "((EMAIL))" if a known domain pattern is detected,
        otherwise None.
    """
    if not isinstance(text, str):
        return None

    text = text.strip().lower()
    if not text:
        return None

    # Remove everything except letters and numbers
    compact_text = re.sub(r"[^a-z0-9]", "", text)

    for domain in DOMINIOS_EMAIL_COMUNS:
        normalized_domain = re.sub(r"[^a-z0-9]", "", domain.lower())

        if normalized_domain in compact_text:
            return "EMAIL"

    return None


def flag_too_many_names(text: str, *, max_tokens: int = 6) -> str | None:
    """
    Flag text if it contains more tokens than the allowed threshold.

    Tokenization is performed using the primitive tokenizer,
    which normalizes whitespace and converts text to lowercase.

    Args:
        text: Input string to evaluate.
        max_tokens: Maximum allowed number of tokens before triggering the flag.

    Returns:
        "TOO_MANY_NAMES" if the number of tokens exceeds the threshold,
        otherwise None.
    """
    tokens = tokenize_words(text)

    if len(tokens) > max_tokens:
        return "TOO_MANY_NAMES"

    return None


def evaluate_name_flags(
        text: Optional[str],
        *,
        min_length: int = 12,
        max_tokens: int = 6,
) -> List[str]:
    """
    Evaluate multiple name-related validation rules and return all triggered flags.

    This function composes independent domain rules:
        - flag_long_name
        - flag_email
        - flag_too_many_names

    The function is deterministic and side effect free.

    Args:
        text: Input string to evaluate.
        min_length: Minimum token length for LONG_NAME flag.
        max_tokens: Maximum allowed tokens before TOO_MANY_NAMES flag.

    Returns:
        A list of triggered flag identifiers.
        Returns an empty list if no rules are triggered.

    Notes:
        - Order of evaluation is fixed and deterministic.
        - No rule overrides another.
    """
    if not isinstance(text, str):
        return []

    text = text.strip()
    if not text:
        return []

    flags: List[str] = []

    long_name_flag = flag_long_name(text, min_length=min_length)
    if long_name_flag:
        flags.append(long_name_flag)

    email_flag = flag_email(text)
    if email_flag:
        flags.append(email_flag)

    too_many_flag = flag_too_many_names(text, max_tokens=max_tokens)
    if too_many_flag:
        flags.append(too_many_flag)

    return flags


def remove_invalid_terms(text: str) -> str:
    """
    Remove predefined invalid terms from text.

    The function performs a case-insensitive match against a predefined
    collection of invalid terms and removes full-word occurrences,
    optionally followed by a period.

    Args:
        text: Input string to sanitize.

    Returns:
        Cleaned string with invalid terms removed.
        Returns an empty string if input is not a string.
    """
    if not isinstance(text, str):
        return ""

    invalid_terms = (
            set(titulos_profissoes)
            | set(partidos_politicos)
            | set(universidades_federais)
            | set(ufs_brasil)
    )

    if not invalid_terms:
        return text.strip()

    pattern = r"\b(" + "|".join(re.escape(term) for term in invalid_terms) + r")\.?\b"

    cleaned_text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text).strip()

    return cleaned_text


def is_linguistically_invalid_name(text: str) -> bool:
    """
    Check whether a name-like text is linguistically invalid based on forbidden terms.

    The check is case-insensitive and matches whole terms using word boundaries.

    Args:
        text: Input string to evaluate.

    Returns:
        True if the input is not a string or if any invalid term is found; otherwise False.
    """
    if not isinstance(text, str):
        return True

    invalid_terms = (
            RELACOES_FAMILIARES
            | ENTIDADES_RELIGIOSAS
            | FRASES_RELIGIOSAS
            | RESPOSTAS_INVALIDAS
            | TOKENS_INVALIDOS_SOLOS
    )

    if not invalid_terms:
        return False

    pattern = r"\b(" + "|".join(re.escape(term) for term in invalid_terms) + r")\b"

    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def text_contains_letters(text: str) -> bool:
    """
    Check whether the text contains at least one Latin letter
    (including accented characters).

    Args:
        text: Input string to evaluate.

    Returns:
        True if at least one letter is found; False otherwise.
        Returns False if input is not a string.
    """
    if not isinstance(text, str):
        return False

    return bool(re.search(r"[A-Za-zÀ-ÿ]", text))


def clean_name_domain_pipeline(text: str, *, keep_numbers: bool = False) -> str | None:
    """
    Clean a raw text into a name-like string or return None if invalid.

    This function is domain-level: it composes existing rules and primitives,
    remains deterministic, and avoids side effects.

    Args:
        text: Raw input string.
        keep_numbers: If True, skips character normalization that would remove digits.

    Returns:
        A cleaned name-like string if valid; otherwise None.
    """
    if not isinstance(text, str):
        return None

    text = text.strip()
    if not text:
        return None

    text = remove_invalid_terms(text)

    if not keep_numbers:
        text = normalize_person_name_characters(text)

    if is_linguistically_invalid_name(text):
        return None

    if not text_contains_letters(text):
        return None

    return text
