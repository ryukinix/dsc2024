import pandas as pd
import os
from pathlib import Path
from functools import lru_cache

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
