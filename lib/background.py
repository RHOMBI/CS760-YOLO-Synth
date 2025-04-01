from typing import Tuple
from PIL import Image
import numpy as np
import random
from dataclasses import dataclass

@dataclass
class RandomNoiseBackground:
    size: int = 1

    def generate_background(self, res_x: int, res_y: int):
        noise_array = np.random.randint(0, 256, (res_y, res_x, 3), dtype=np.uint8)
        return Image.fromarray(noise_array, "RGB")


@dataclass
class PerlinNoiseBackground:
    size: int = 10
    colour_1: Tuple[int, int, int] = (0, 0, 0)
    colour_2: Tuple[int, int, int] = (255, 255, 255)

    def generate_background(self, res_x: int, res_y: int):
        #TODO
        noise_array = np.random.randint(0, 256, (res_y, res_x, 3), dtype=np.uint8)
        return Image.fromarray(noise_array, "RGBA")