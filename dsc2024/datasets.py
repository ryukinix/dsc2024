import os
from pathlib import Path

import pandas

_base_path = os.path.dirname(os.path.dirname(__file__))
datasets_dir = Path(os.path.join(_base_path, "datasets"))


def get_public_dataset() -> pandas.DataFrame:
    return pandas.read_csv(datasets_dir / "public.csv")
