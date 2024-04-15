import os
from pathlib import Path
from typing import Optional

import pandas

from dsc2024 import handling

_base_path = os.path.dirname(os.path.dirname(__file__))
datasets_dir = Path(os.path.join(_base_path, "datasets"))


def get_public_dataset(
    parse_hora_ref: bool = True,
    expand_metar_and_metaf: bool = True,
    sampling: Optional[int] = None,
    set_flightid_as_index: bool = True
) -> pandas.DataFrame:
    df = pandas.read_csv(datasets_dir / "public.csv")

    if sampling:
        df = df.sample(n=sampling)
    if parse_hora_ref:
        df.hora_ref = handling.parse_hora_ref_as_series(df.hora_ref)
    if expand_metar_and_metaf:
        df = handling.expand_metar_and_metaf_features(df)
    if set_flightid_as_index:
        df.set_index("flightid", inplace=True)
    return df


def get_train_dataset(sampling: Optional[int] = None):
    """Get all rows with 'espera' labeled as 0 or 1"""
    df = get_public_dataset(sampling=sampling)
    mask = df.notna().espera
    return df[mask]


def get_test_dataset(sampling: Optional[int] = None):
    """Only get rows with 'espera' with missing-values"""
    df = get_public_dataset(sampling=sampling)
    mask = df.isna().espera
    return df[mask]
