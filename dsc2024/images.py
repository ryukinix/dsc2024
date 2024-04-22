from typing import Tuple, List
from io import BytesIO

from dsc2024.datasets import get_image_mask_points

import requests
from PIL import Image as PIL_Image

PILCropMask = Tuple[int, int, int, int]


def generate_pil_crop_mask(mask_points: List[Tuple[int, int]]) -> PILCropMask:
    """Create from our four-point rectangle mask the PIL crop mask"""
    x = [x for x, _ in mask_points]
    y = [y for _, y in mask_points]
    return (min(x), min(y), max(x), max(y))


def read_image_from_response_and_cropit(
    response: requests.Response,
    mask: PILCropMask
) -> PIL_Image.Image:
    """Read from a successful response and generate a image cropped"""
    img = PIL_Image.open(BytesIO(response.content))
    img_cropped = img.crop(mask)
    return img_cropped


def download_image_and_cropit(url: str) -> PIL_Image.Image:
    mask = generate_pil_crop_mask(get_image_mask_points())
    response = requests.get(url)
    return read_image_from_response_and_cropit(response, mask)
