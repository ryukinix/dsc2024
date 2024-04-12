import os
from pathlib import Path

import pandas

from dsc2024 import handling

_base_path = os.path.dirname(os.path.dirname(__file__))
datasets_dir = Path(os.path.join(_base_path, "datasets"))


def get_public_dataset(parse_hora_ref=True) -> pandas.DataFrame:
    df = pandas.read_csv(datasets_dir / "public.csv")
    if parse_hora_ref:
        df.hora_ref = handling.parse_hora_ref_as_series(df.hora_ref)
    return df
