"""
Data Handling common tasks transformations and normalization
"""

from typing import Optional, List

import pandas
import datetime

from metpy.io.metar import Metar, parse_metar, ParseError


def parse_metar_as_dataframe(
    df: pandas.DataFrame,
    metar_column="metar"
) -> pandas.DataFrame:
    """Expected to hora_ref column be already normalized"""
    index = df.index
    metars: List[Optional[Metar]] = []
    for _, row in df.iterrows():
        metar_value = row[metar_column]
        try:
            if not isinstance(metar_value, str):
                metars.append(None)
                continue
            if metar_column == "metaf":
                metar_value = metar_value.replace("METAF", "METAR")
            hora_ref = row["hora_ref"]
            year, month = hora_ref.year, hora_ref.month
            metar_parsed = parse_metar(metar_value, year=year, month=month)
            metars.append(metar_parsed)
        except ParseError:
            metars.append(None)

    return pandas.DataFrame(metars, index=index)


def parse_hora_ref_as_series(series: pandas.Series) -> pandas.Series:
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    return series.apply(lambda s: datetime.datetime.strptime(s, date_format))
