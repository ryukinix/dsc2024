import os
import json
from pathlib import Path
from typing import Optional, List, Tuple
from functools import lru_cache

import pandas

from dsc2024 import handling

_base_path = os.path.dirname(os.path.dirname(__file__))
datasets_dir = Path(os.path.join(_base_path, "datasets"))
image_embedding_path = datasets_dir / "images.pkl.xz"


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


def _generate_raw_data_kwargs(raw_data: bool = True):
    """Generate arguments to not add extra parsing"""
    kwargs = {}
    if raw_data:
        kwargs = {
            "expand_metar_and_metaf": False,
            "set_flightid_as_index": False,
            "parse_hora_ref": False,
        }
    return kwargs


def get_train_dataset(sampling: Optional[int] = None,
                      raw_data: bool = False):
    """Get all rows with 'espera' labeled as 0 or 1"""
    raw_kwargs = _generate_raw_data_kwargs(raw_data)
    df = get_public_dataset(sampling=sampling, **raw_kwargs)
    mask = df.notna().espera
    return df[mask]


def get_test_dataset(sampling: Optional[int] = None,
                     raw_data: bool = False):
    """Only get rows with 'espera' with missing-values"""
    raw_kwargs = _generate_raw_data_kwargs(raw_data)
    df = get_public_dataset(sampling=sampling, **raw_kwargs)
    mask = df.isna().espera
    return df[mask]


def save_image_embedding(df: pandas.DataFrame):
    df.to_pickle(image_embedding_path)


def get_image_embedding() -> pandas.DataFrame:
    return pandas.read_pickle(image_embedding_path)


@lru_cache
def get_image_mask_points() -> List[Tuple[int, int]]:
    fpath = datasets_dir / "image-mask" / "image-mask.json"
    with fpath.open(encoding="UTF-8") as source:
        image_mask = json.load(source)[0]
    return [
        (round(p["x"]), round(p["y"]))
        for p in image_mask["content"]
    ]
