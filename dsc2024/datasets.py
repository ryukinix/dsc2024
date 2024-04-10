import os
import zipfile
from io import StringIO
from urllib.parse import urlparse, unquote
from urllib import request

import pandas
import requests

_base_path = os.path.dirname(os.path.dirname(__file__))
datasets_dir = os.path.join(_base_path, "datasets")

datasets_urls = {
    "reuter_50_50": "https://archive.ics.uci.edu/static/public/217/reuter+50+50.zip",  # noqa
    "br_worst_places_to_work": "https://docs.google.com/spreadsheets/d/1u1_8ND_BY1DaGaQdu0ZRZPebrOaTJekE9hyw_7BAlzw/export?format=csv"   # noqa
}


def _create_datasets_directory():
    os.makedirs(datasets_dir, exist_ok=True)


def _get_file_name_url(url: str) -> str:
    url_object = urlparse(url)
    path = unquote(url_object.path)
    file_name = path.strip("/").split("/")[-1]
    return file_name


def _download_file(url: str, fpath: str):
    request.urlretrieve(url, fpath)


def download_dataset(url: str) -> str:
    _create_datasets_directory()
    fname = _get_file_name_url(url)
    fpath = os.path.join(datasets_dir, fname)
    if not os.path.exists(fpath):
        print(f"[+] Downloading file={fpath}")
        _download_file(url, fpath)

    return fpath


def get_dataset_reuter_50_50() -> dict:
    """Author recognition datasets with 50 authors and 50 texts for each one.

    Returns
    -------
    A dictionary with two pandas dataframes, for train and other for
    test.
    """
    fpath = download_dataset(datasets_urls["reuter_50_50"])
    columns = ["env", "author", "text", "text_id"]
    values = []
    with zipfile.ZipFile(fpath) as z:
        for filename in z.namelist():
            if not z.getinfo(filename).is_dir():
                envdir, author, text_id = filename.split("/")
                env = "test" if "test" in envdir else "train"
                value = [
                    env,
                    author,
                    z.open(filename).read().decode("utf-8"),
                    text_id
                ]
                values.append(value)
    df = pandas.DataFrame(values, columns=columns)
    return {
        "test": df[df.env == "test"],
        "train": df[df.env == "train"]
    }


def get_dataset_br_worst_places_to_work() -> pandas.DataFrame:
    response = requests.get(datasets_urls["br_worst_places_to_work"])
    response.encoding = 'utf-8'  # fix encoding
    return pandas.read_csv(StringIO(response.text))
