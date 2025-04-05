from lib.background import RandomNoiseBackground, PerlinNoiseBackground, RandomNoiseReferenceImageBackground

from dataclasses import dataclass, field
from pathlib import Path
import shutil
from typing import List, Union

from PIL import Image
import numpy as np
import random


@dataclass
class MutationParameters:
    #shear in the x,y directions
    shear_x: float = 1
    shear_y: float = 1

    #min and max scaling of the original sprite (uniform scaling)
    scale_min: float = 1
    scale_max: float = 5

    rotation: bool = False

    background: Union[RandomNoiseBackground, PerlinNoiseBackground, RandomNoiseReferenceImageBackground] = field(default_factory=RandomNoiseBackground)

    def generate_background(self, res_x: int, res_y: int):
        return self.background.generate_background(res_x, res_y)


def generate_dataset(
        asset_paths: List[Path],
        save_path: Path,
        count: int,
        params: MutationParameters,
        res_x: int = 1000,
        res_y: int = 1000,
):

    for i in range(0, count):
        reference_image = random.choice(asset_paths)
        with Image.open(reference_image).convert("RGBA") as img:
            reference_img_width, reference_img_height = img.size
            background = params.generate_background(res_x, res_y)
            background_width, background_height = background.size

            #do not scale the image so large that it is larger than the background
            params.scale_max = min(params.scale_max, background_width / reference_img_width, background_height / reference_img_height)
            params.scale_min = min(params.scale_min, params.scale_max)

            #place the image at a random position on the background
            random_offset_x = random.randint(0, background_width - reference_img_width)
            random_offset_y = random.randint(0, background_height - reference_img_height)

            #randomly scale the image (both axis uniformly)
            scale = random.uniform(params.scale_min, params.scale_max)

            img = img.resize((int(reference_img_width * scale), int(reference_img_height * scale)), Image.LANCZOS)

            background.paste(img, (random_offset_x, random_offset_y), img)

            background.save(save_path / f"{i}.png", format="PNG")



    

