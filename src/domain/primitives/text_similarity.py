import jellyfish


def extract_prefix(text: str, n: int = 3) -> str:
    """
    Extract the first `n` characters from a string.

    If the string has fewer than `n` characters, the entire string
    is returned. Returns an empty string for invalid or blank input.

    Args:
        text: Input string.
        n: Number of leading characters to extract.

    Returns:
        A string containing the first `n` characters of the input.
    """
    if not isinstance(text, str) or not text:
        return ""

    text = text.strip()
    return text[:n]


def has_same_prefix(text1: str, text2: str, n: int = 3) -> bool:
    """
    Check whether two strings share the same prefix of length `n`.

    Args:
        text1: First string to compare.
        text2: Second string to compare.
        n: Number of leading characters to evaluate.

    Returns:
        True if both strings share the same prefix of length `n`,
        otherwise False.
    """
    prefix1 = extract_prefix(text1, n)
    prefix2 = extract_prefix(text2, n)

    return prefix1 == prefix2


def jaro_winkler_score(a: str, b: str) -> float:
    """
    Compute the Jaro-Winkler similarity score between two strings.

    Args:
        a: First string to compare.
        b: Second string to compare.

    Returns:
        A float between 0.0 and 1.0 representing the similarity score.
        Returns 0.0 if either input is invalid or blank.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0

    a = a.strip()
    b = b.strip()

    if not a or not b:
        return 0.0

    return jellyfish.jaro_winkler_similarity(a, b)


def is_similar_jaro_winkler(a: str, b: str, threshold: float) -> bool:
    """
    Determine whether two strings are similar based on the
    Jaro-Winkler similarity score and a minimum threshold.

    Args:
        a: First string to compare.
        b: Second string to compare.
        threshold: Minimum similarity score required to consider the strings similar.

    Returns:
        True if the similarity score is greater than or equal to `threshold`,
        otherwise False.

    Raises:
        ValueError: If `threshold` is not a numeric value.
    """
    if not isinstance(threshold, (int, float)):
        raise ValueError(f"Invalid threshold: {threshold}")

    score = jaro_winkler_score(a, b)

    return score >= threshold


def group_similar_strings(
        values: list[str],
        *,
        prefix_length: int = 3,
        jaro_threshold: float = 0.88,
) -> list[list[str]]:
    """
    Group similar strings based on prefix matching or Jaro-Winkler similarity.

    Two consecutive values are grouped together when they share the same prefix
    of length `prefix_length` or when their Jaro-Winkler similarity score is
    greater than or equal to `jaro_threshold`.

    Notes:
        This function groups only adjacent items in the provided order. If you
        need order-independent clustering, sort or pre-process the input first.

    Args:
        values: List of strings to group.
        prefix_length: Number of leading characters used for prefix comparison.
        jaro_threshold: Minimum similarity score required to group values.

    Returns:
        A list of groups, where each group is a list of similar strings.

    Raises:
        ValueError: If the input list is empty.
    """
    if not values:
        raise ValueError("Input list cannot be empty.")

    values = [v.strip() for v in values if v and v.strip()]

    if not values:
        return []

    groups: list[list[str]] = []
    current_group: list[str] = [values[0]]

    for i in range(1, len(values)):
        prev = current_group[-1]
        curr = values[i]

        are_similar = (
                has_same_prefix(prev, curr, n=prefix_length)
                or is_similar_jaro_winkler(prev, curr, threshold=jaro_threshold)
        )

        if are_similar:
            current_group.append(curr)
        else:
            groups.append(current_group)
            current_group = [curr]

    if current_group:
        groups.append(current_group)

    return groups
