from src.domain.primitives.text_similarity import jaro_winkler_score
from src.domain.primitives.text_patterns import EMAIL_REGEX
from typing import Optional


def choose_best_match(
        groups: list[list[str]],
        candidates: list[str],
        high_threshold: float = 0.92,
) -> list[Optional[str]]:
    """
    Choose the best candidate match for each group of string variants using
    Jaro-Winkler similarity.

    Rules:
        - If a group is empty, returns None for that group.
        - If a group has size 1, returns the single value.
        - Exact match stops the search immediately for that group.
        - Similarity >= `high_threshold` stops the search immediately for that group.
        - Preserves the original order of groups.

    Args:
        groups: List of groups containing string variants.
        candidates: Candidate strings to match against.
        high_threshold: Similarity threshold considered a strong match.

    Returns:
        A list containing the best candidate for each group, or None when no
        match is available.
    """
    results: list[Optional[str]] = []

    for group in groups:
        if not group:
            results.append(None)
            continue

        if len(group) == 1:
            results.append(group[0])
            continue

        best_score = -1.0
        best_match: Optional[str] = None

        for variant in group:
            v_norm = variant.strip()

            for candidate in candidates:
                c_norm = candidate.strip()

                if v_norm == c_norm:
                    best_match = candidate
                    best_score = 1.0
                    break

                score = jaro_winkler_score(v_norm, c_norm)

                if score > best_score:
                    best_score = score
                    best_match = candidate

                if score >= high_threshold:
                    break

            if best_score == 1.0 or best_score >= high_threshold:
                break

        results.append(best_match)

    return results


def is_valid_email(value: str) -> bool:
    if not isinstance(value, str):
        return False
    return bool(EMAIL_REGEX.match(value.strip()))
