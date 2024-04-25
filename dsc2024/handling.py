"""
Data Handling common tasks transformations and normalization
"""

from typing import Optional, List

import pandas as pd
import datetime

from metpy.io.metar import Metar, parse_metar, ParseError


def _create_default_metar_value() -> Metar:
    fields = Metar._fields
    values = {f: None for f in fields}
    return Metar(**values)


def parse_metar_as_dataframe(
    df: pd.DataFrame,
    metar_column="metar"
) -> pd.DataFrame:
    """Expected to hora_ref column be already normalized"""
    index = df.index.copy()
    metars: List[Optional[Metar]] = []
    default_metar_value = _create_default_metar_value()
    for i, row in df.iterrows():
        metar_value = row[metar_column]
        try:
            if not isinstance(metar_value, str):
                metars.append(default_metar_value)
                continue
            if metar_column == "metaf":
                metar_value = metar_value.replace("METAF", "METAR")
            hora_ref = row["hora_ref"]
            year, month = hora_ref.year, hora_ref.month
            metar_parsed = parse_metar(metar_value, year=year, month=month)
            metars.append(metar_parsed)
        except ParseError as e:
            print(f"dataset row:{i}", e)
            metars.append(default_metar_value)

    return pd.DataFrame.from_records(metars, index=index, columns=Metar._fields)


def parse_hora_ref_as_series(series: pd.Series) -> pd.Series:
    """Parse series of hora_ref string 2022-06-01T01:00:00Z as datetime"""
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    return series.apply(lambda s: datetime.datetime.strptime(s, date_format))


def expand_metar_and_metaf_features(df: pd.DataFrame) -> pd.DataFrame:
    """Expand attributes of metar and metaf columns"""
    df_metar = parse_metar_as_dataframe(df, metar_column="metar").add_prefix("metar_")  # noqa
    df_metaf = parse_metar_as_dataframe(df, metar_column="metaf").add_prefix("metaf_")  # noqa
    assert len(df_metaf.columns) > 1, "metaf parsing failed, try again"
    df_metar_and_metaf = df_metar.join(df_metaf, how="left")
    return df.join(df_metar_and_metaf).drop(columns=["metaf", "metar"])


def add_image_vectors(
    df: pd.DataFrame,
    image_vectors: pd.DataFrame,
    naive_imputation: bool = True
) -> pd.DataFrame:
    # imputation
    # assume df index is already flightd
    image_vectors.set_index("flightid", inplace=True)
    if naive_imputation:
        mean_vector = image_vectors["vector"].mean()
        # FIXME: doesn't work with vectors
        # image_vectors.fillna(mean_vector)
        nulls = image_vectors[image_vectors.vector.isna()]

        for i in nulls.index:
            image_vectors.at[i, "vector"] = mean_vector

    return df.join(image_vectors)
