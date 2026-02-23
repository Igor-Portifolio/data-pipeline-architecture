from src.domain.vocabulary.voc_endereco import *
import re
from typing import Any
from typing import Mapping


def _extract_vocabulary_tokens(vocabulary: dict) -> set[str]:
    """
    Extract all textual variations from a vocabulary dictionary.

    Args:
        vocabulary: Dictionary containing canonical terms and their variations.

    Returns:
        A set containing all canonical terms and their variations in lowercase.
    """
    tokens = set()

    for group in vocabulary.values():
        for canonical, variations in group.items():
            tokens.add(canonical.lower())
            tokens.update(v.lower() for v in variations)

    return tokens


def tokenize_address(text: str, vocabulary: dict) -> list[str]:
    """
    Tokenize an address string, splitting letter+number sequences only when the
    textual part exists in the provided vocabulary.

    Args:
        text: Raw address text to tokenize.
        vocabulary: Vocabulary dictionary containing canonical terms and variations.

    Returns:
        A list of tokens extracted from the normalized address text. Returns an empty
        list when the input is not a string or when it is blank.
    """
    if not isinstance(text, str):
        return []

    text = text.strip()
    if not text:
        return []

    vocab_tokens = _extract_vocabulary_tokens(vocabulary)

    # Normalize common separators.
    text = re.sub(r"[.,-]", " ", text)

    def _split_if_in_vocab(match: re.Match) -> str:
        letters = match.group(1)
        number = match.group(2)

        if letters.lower() in vocab_tokens:
            return f"{letters} {number}"

        return match.group(0)

    text = re.sub(r"([A-Za-zÀ-ÿ]+)(\d+)", _split_if_in_vocab, text)

    text = re.sub(
        r"(\d+)([A-Za-zÀ-ÿ]+)",
        lambda m: f"{m.group(1)} {m.group(2)}"
        if m.group(2).lower() in vocab_tokens
        else m.group(0),
        text,
    )

    # Keep only letters, numbers, and whitespace.
    text = re.sub(r"[^A-Za-zÀ-ÿ0-9\s]", " ", text)

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    return text.split(" ")


def expand_tokens_using_vocabulary(tokens: list[str], vocabulary: dict) -> list[str]:
    """
    Replace known tokens with their canonical forms using a hierarchical vocabulary
    (e.g., an address vocabulary).

    Preserves token order and count.

    Args:
        tokens: List of tokens to standardize.
        vocabulary: Hierarchical vocabulary mapping categories to canonical forms and
            their textual variations.

    Returns:
        A list of tokens where recognized variations are replaced by their canonical
        forms. Returns an empty list if `tokens` is not a list.
    """
    if not isinstance(tokens, list):
        return []

    standardized_tokens = []

    for token in tokens:
        if not isinstance(token, str):
            standardized_tokens.append(token)
            continue

        token_lower = token.lower()
        replaced = False

        for _, group in vocabulary.items():
            for canonical_form, variations in group.items():
                if token_lower in variations:
                    standardized_tokens.append(canonical_form)
                    replaced = True
                    break
            if replaced:
                break

        if not replaced:
            standardized_tokens.append(token)

    return standardized_tokens


def reorder_simple_vocabulary_pair(tokens: list[Any]) -> list[Any]:
    """
    Reorder simple token pairs into the format [vocabulary, value] when the
    list length is exactly two.

    If the structure does not match the expected pattern, the original list
    is returned unchanged.

    Args:
        tokens: List of tokens that may contain a vocabulary term and a value.

    Returns:
        A reordered list in the format [vocabulary, value] when applicable,
        otherwise the original list.
    """
    if not isinstance(tokens, list):
        return tokens

    if len(tokens) > 2:
        return tokens

    if len(tokens) != 2:
        return tokens

    a, b = tokens

    def _is_value(x: Any) -> bool:
        return isinstance(x, (int, float)) or (
                isinstance(x, str) and x.isdigit()
        )

    def _is_vocabulary(x: Any) -> bool:
        return isinstance(x, str) and not _is_value(x)

    if _is_vocabulary(a) and _is_value(b):
        return [a, b]

    if _is_value(a) and _is_vocabulary(b):
        return [b, a]

    return tokens


def rebuild_text(tokens: list[Any]) -> str:
    """
    Rebuild a readable string from a list of tokens.

    Args:
        tokens: List of tokens to be converted into a string.

    Returns:
        A whitespace-normalized string built from the provided tokens.
        Returns an empty string if `tokens` is not a list.
    """
    if not isinstance(tokens, list):
        return ""

    parts = [str(token) for token in tokens if token is not None]

    text = " ".join(parts)
    text = " ".join(text.split())

    return text


def address_domain_pipeline(text: str) -> str:
    """
    Execute the domain-level address normalization pipeline.

    This function tokenizes the input text, expands tokens using the
    address vocabulary, reorders simple vocabulary-value pairs,
    and returns a normalized uppercase string.

    Args:
        text: Raw address string to normalize.

    Returns:
        A normalized address string in uppercase format.
        Returns an empty string if `text` is not a string.
    """
    if not isinstance(text, str):
        return ""

    tokens = tokenize_address(text, VOCABULARIO_ENDERECO)
    tokens = expand_tokens_using_vocabulary(tokens, VOCABULARIO_ENDERECO)
    tokens = reorder_simple_vocabulary_pair(tokens)

    return rebuild_text(tokens).upper()


def tokenize_district(text: str, vocabulary: Mapping[str, list[str]]) -> list[str]:
    """
    Perform tolerant tokenization of a district string.

    Splits concatenated tokens only when they start with a known
    abbreviation from the provided vocabulary and are not already
    an exact canonical form.

    Args:
        text: Raw district string to tokenize.
        vocabulary: Mapping of canonical forms to their known variations.

    Returns:
        A list of tokens derived from the input string.
        Returns an empty list if `text` is not a string or is blank.
    """
    if not isinstance(text, str):
        return []

    text = text.strip().upper()
    if not text:
        return []

    canonical_forms: set[str] = {k.upper() for k in vocabulary.keys()}
    valid_prefixes: set[str] = set()

    for variations in vocabulary.items():
        for variation in variations:
            valid_prefixes.add(variation.upper())

    sorted_prefixes: list[str] = sorted(valid_prefixes, key=len, reverse=True)

    tokens = re.split(r"\s+", text)
    result = []

    for token in tokens:
        if token in canonical_forms:
            result.append(token)
            continue

        separated = False

        for prefix in sorted_prefixes:
            if token.startswith(prefix) and token != prefix:
                remainder = token[len(prefix):]

                if remainder.isalpha():
                    result.append(prefix)
                    result.append(remainder)
                    separated = True
                    break

        if not separated:
            result.append(token)

    return result


def district_domain_pipeline(texto: str) -> str:
    """
    Execute the domain-level district normalization pipeline.

    This function tokenizes the input text using the district vocabulary,
    expands recognized variations into their canonical forms, and returns
    a normalized uppercase string.

    Args:
        texto: Raw district string to normalize.

    Returns:
        A normalized district string in uppercase format.
        Returns an empty string if the input is not a string.
"""

    if not isinstance(texto, str):
        return ""

    tokens = tokenize_district(texto, VOCABULARIO_BAIRRO)
    tokens = expand_tokens_using_vocabulary(tokens, VOCABULARIO_BAIRRO)

    return rebuild_text(tokens).upper()
