from lib.background import RandomNoiseBackground, PerlinNoiseBackground

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
    scale_max: float = 1

    rotation: bool = False

    background: Union[RandomNoiseBackground, PerlinNoiseBackground] = field(default_factory=RandomNoiseBackground)

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
            width, height = img.size

            # make sure the reference image is not larger than the background
            assert(width <= res_x)
            assert(height <= res_y)
            
            background = params.generate_background(res_x, res_y)
            background.paste(img, (0, 0), img)

            background.save(save_path / f"{i}.png", format="PNG")



    

