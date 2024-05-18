from functools import lru_cache
from pathlib import Path
import os

import pandas as pd

_base_path = os.path.dirname(os.path.dirname(__file__))
_datasets_dir = os.environ.get(
    "DSC2024_DATASETS_DIR",
    os.path.join(_base_path, "datasets")
)
datasets_dir = Path(_datasets_dir)


@lru_cache
def get_airport_geolocalization() -> dict:
    """
    {
        "SBSP": ["longitude", "latitude"]
    }
    """
    df = pd.read_csv(datasets_dir / "airport_geolocalization.csv")
    airport_localizations = {}
    for row in df.itertuples():
        airport_localizations[row.airport] = [row.longitude, row.latitude]
    return airport_localizations


@lru_cache
def get_catboost_regression() -> pd.DataFrame:
    parse_dates = ["dt_dep", "dt_arr"]
    df = pd.read_csv(
        datasets_dir / "catboost_regression.csv",
        parse_dates=parse_dates,
    )
    # df.sort_values(by="espera", inplace=True)
    selected_columns = ["origem", "destino", "dt_dep", "dt_arr", "espera"]
    return df[selected_columns]
