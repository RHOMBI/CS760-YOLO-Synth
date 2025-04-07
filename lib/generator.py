from lib.background import RandomNoiseBackground, PerlinNoiseBackground, RandomNoiseReferenceImageBackground
from lib.annotate import paste_sprite

import os
from dataclasses import dataclass, field
from pathlib import Path
import shutil
from typing import List, Union

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random

@dataclass
class MutationParameters:
    #TODO shear in the x,y directions
    shear_x: float = 1
    shear_y: float = 1

    #min and max scaling of the original sprite (uniform scaling)
    scale_min: float = 0.4
    scale_max: float = 4

    brightness_min: float = 0.7
    brightness_max: float = 1.3

    contrast_min: float = 0.7
    contrast_max: float = 1.5

    sharpness_min: float = 1.5
    sharpness_max: float = 3.0

    blur_min: float = 0.5
    blur_max: float = 2.5

    rotation_min: float = -45
    rotation_max: float = 45

    effect_count = 1

    background: Union[RandomNoiseBackground, PerlinNoiseBackground, RandomNoiseReferenceImageBackground] = field(default_factory=RandomNoiseBackground)

    enabled_ops: List[str] = field(default_factory=lambda: ["rotate", "scale", "flip", "brightness", "contrast", "sharpen", "blur"])

    def generate_background(self, res_x: int, res_y: int, reference_images: List[str]) -> Image.Image:
        return self.background.generate_background(res_x, res_y, reference_images)
    
    def apply_rotate(self, img):
        angle = random.randint(self.rotation_min, self.rotation_max)
        return img.rotate(angle, expand=True)

    def apply_scale(self, img):
        scale = random.uniform(self.scale_min, self.scale_max)
        w, h = img.size
        
        #TODO investigate what is Image.LANCZOS
        sprite_image = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        #sprite_image = img.resize((int(w * scale), int(h * scale)))
        return sprite_image
    
    def apply_flip(self, img):
        return img.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM]))

    def apply_brightness(self, img):
        factor = random.uniform(self.brightness_min, self.brightness_max)
        return ImageEnhance.Brightness(img).enhance(factor)

    def apply_contrast(self, img):
        factor = random.uniform(self.contrast_min, self.contrast_max)
        return ImageEnhance.Contrast(img).enhance(factor)

    def apply_sharpen(self, img):
        factor = random.uniform(self.sharpness_min, self.sharpness_max)
        return ImageEnhance.Sharpness(img).enhance(factor)

    def apply_blur(self, img):
        radius = random.uniform(self.blur_min, self.blur_max)
        return img.filter(ImageFilter.GaussianBlur(radius))
    
    @property
    def augmentation_ops(self):
        return {
            "rotate": self.apply_rotate,
            "scale": self.apply_scale,
            "flip": self.apply_flip,
            "brightness": self.apply_brightness,
            "contrast": self.apply_contrast,
            "sharpen": self.apply_sharpen,
            "blur": self.apply_blur
        }

    def apply_mutations(self, img, count: int):
        enabled_ops = self.enabled_ops.copy()

        for _ in range(count):
            if len(enabled_ops) == 0:
                print("Warning: Operations exhausted")
                return img
            
            op_name = random.choice(enabled_ops)
            enabled_ops.remove(op_name)
            op = self.augmentation_ops.get(op_name)
            if op is None:
                raise ValueError(f"Unrecognised operation enabled: \"{op_name}\"")
            img = op(img)
        
        return img


def generate_dataset(
        sprites_path: Path,
        backgrounds_path: Path,
        save_path: Path,
        count: int,
        params: MutationParameters,
        default_res_x: int = 1000,
        default_res_y: int = 1000,
):
    
    sprite_files = [os.path.join(sprites_path, f) for f in os.listdir(sprites_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    background_files = [os.path.join(backgrounds_path, f) for f in os.listdir(backgrounds_path) if f.endswith(('png', 'jpg', 'jpeg'))]

    for i in range(0, count):
        img_class = random.randrange(len(sprite_files))
        sprite_image = Image.open(sprite_files[img_class]).convert("RGBA")
        background_image = params.generate_background(default_res_x, default_res_y, background_files)

        sprite_image = params.apply_mutations(sprite_image, 1)

        generated_image, generated_annotation = paste_sprite(background=background_image, sprite=sprite_image, class_id=img_class)
        
        img_name = f"gen_img_{i:04d}.png"
        generated_image.save(os.path.join(save_path, img_name))

        annotation_name = f"gen_img_{i:04d}.txt"
        with open(os.path.join(save_path, annotation_name), "w") as f:
            f.write(generated_annotation)



    

