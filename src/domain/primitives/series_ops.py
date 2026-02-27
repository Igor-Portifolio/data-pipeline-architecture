from typing import cast
import pandas as pd


def safe_replace(
    serie: pd.Series,
    to_replace,
    value,
) -> pd.Series:
    result = serie.replace(to_replace, value, inplace=False)
    return cast(pd.Series, cast(object, result))

