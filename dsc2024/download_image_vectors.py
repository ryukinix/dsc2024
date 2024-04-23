from typing import Optional
from dataclasses import dataclass
import os

from requests.exceptions import HTTPError
from tqdm_joblib import tqdm_joblib

import joblib
import numpy as np
import pandas as pd
import requests
from loguru import logger


from dsc2024 import datasets
from dsc2024 import features
from dsc2024 import images


# FIXME(@lerax): ter 23 abr 2024 14:43:39
# global variables are only acceptable here because this is a script
# but would be nice to refactor this
logger.debug("loading vision transformers as global variables")
MASK = images.generate_pil_crop_mask(datasets.get_image_mask_points())
PREPROCESSOR, VIT = features.load_transformer_feature_extractor()
logger.debug("transformers loaded!")


@dataclass
class FlightImageVector:
    flightd: str
    vector: Optional[np.ndarray]


def download_flight_image_vector(flightid: str, url: Optional[str]) -> FlightImageVector:
    if not isinstance(url, str) or not url:
        return FlightImageVector(flightd=flightid, vector=None)
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPError(f"Failed to retrieve image from url={url} of flightd={flightid}")
    img = images.read_image_from_response_and_cropit(response, MASK)
    vector = features.feature_extraction_from_image(img, PREPROCESSOR, VIT)
    return FlightImageVector(
        flightd=flightid,
        vector=vector
    )


def create_delayed_tasks(df: pd.DataFrame):
    return [
        joblib.delayed(download_flight_image_vector)(t.flightid, t.url_img_satelite)
        for t in df.itertuples()
    ]


def download_batch_parallel():
    raw_kwargs = datasets._generate_raw_data_kwargs()
    logger.info("loading dataset with urls for download")
    df = datasets.get_public_dataset(**raw_kwargs)
    n_jobs = os.cpu_count()  # in parallel
    tasks = create_delayed_tasks(df)
    n_tasks = len(tasks)
    logger.info(f"total of jobs: {len(tasks)} | in parallel: {n_jobs}")
    logger.info("starting to download the image vectors")
    with tqdm_joblib(desc="image-vectors", total=n_tasks):
        parallel_pool = joblib.Parallel(n_jobs=n_jobs, prefer="threads")
        df_vectors = pd.DataFrame(parallel_pool(tasks))

    logger.info("saving dataframe")
    datasets.save_image_embedding(df_vectors)


if __name__ == "__main__":
    download_batch_parallel()
