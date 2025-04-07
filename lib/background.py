from typing import List, Tuple
from PIL import Image
import numpy as np
import random
from dataclasses import dataclass

@dataclass
class RandomNoiseBackground:
    size: int = 1

    def generate_background(self, res_x: int, res_y: int, reference_images: List[str]) -> Image.Image:
        noise_array = np.random.randint(0, 256, (res_y, res_x, 3), dtype=np.uint8)
        return Image.fromarray(noise_array, "RGB")


@dataclass
class PerlinNoiseBackground:
    size: int = 10
    colour_1: Tuple[int, int, int] = (0, 0, 0)
    colour_2: Tuple[int, int, int] = (255, 255, 255)

    def generate_background(self, res_x: int, res_y: int, reference_images: List[str]) -> Image.Image:
        #TODO
        noise_array = np.random.randint(0, 256, (res_y, res_x, 3), dtype=np.uint8)
        return Image.fromarray(noise_array, "RGBA")
    
@dataclass
class RandomNoiseReferenceImageBackground:
    noise: float = 0.0

    def generate_background(self, res_x: int, res_y: int, reference_images: List[str] ) -> Image.Image:

        reference_image_path = random.choice(reference_images)
        reference_image = Image.open(reference_image_path).convert("RGBA")
        
        image_width, image_height = reference_image.size
        noise_array = np.random.randint(0, 256, (image_height, image_width, 3), dtype=np.uint8)
        noise_image = Image.fromarray(noise_array, "RGB")
        
        blended_image = Image.blend(reference_image.convert("RGBA"), noise_image.convert("RGBA"), self.noise)
        
        return blended_image