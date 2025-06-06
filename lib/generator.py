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
    scale_min: float = 0.8
    scale_max: float = 1.2

    brightness_min: float = 0.8
    brightness_max: float = 1.2

    contrast_min: float = 0.9
    contrast_max: float = 1.2

    sharpness_min: float = 1.2
    sharpness_max: float = 1.4

    blur_min: float = 0.8
    blur_max: float = 1.2

    rotation_min: float = -1
    rotation_max: float = 1

    effect_count: int = 1

    background: Union[RandomNoiseBackground, PerlinNoiseBackground, RandomNoiseReferenceImageBackground] = field(default_factory=RandomNoiseBackground)

    enabled_ops: List[str] = field(default_factory=lambda: ["scale", "flip", "brightness", "contrast", "sharpen", "blur"])

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
    # -------------- UPDATE: Build a list of sprite paths per class ----------------
    # Each subfolder in sprites_path is one class, containing multiple images.
    class_dirs = [
        os.path.join(sprites_path, d)
        for d in os.listdir(sprites_path)
        if os.path.isdir(os.path.join(sprites_path, d))
    ]

    # sprite_files_by_class[class_id] = [full_path_to_image1, full_path_to_image2, ...]
    sprite_files_by_class = []
    for class_dir in class_dirs:
        image_list = [
            os.path.join(class_dir, f)
            for f in os.listdir(class_dir)
            if f.lower().endswith(('png', 'jpg', 'jpeg'))
        ]
        # Skip empty class folders
        if image_list:
            sprite_files_by_class.append(image_list)

    if not sprite_files_by_class:
        raise ValueError(f"No image files found under any subdirectory of {sprites_path!r}")

    # -------------- ORIGINAL: Load background files --------------------------------
    background_files = [
        os.path.join(backgrounds_path, f)
        for f in os.listdir(backgrounds_path)
        if f.lower().endswith(('png', 'jpg', 'jpeg'))
    ]

    if not background_files:
        raise ValueError(f"No background images found in {backgrounds_path!r}")

    # -------------- GENERATE DATASET LOOP ------------------------------------------
    for i in range(count):
        # 1) create one fresh background per output image
        background_image = params.generate_background(
            default_res_x, default_res_y, background_files
        )

        # 2) accumulate all the annotations for this image here
        annotations = []

        # Place N sprites per generated image (here, N = 5)
        for j in range(5):
            # pick a random class index
            class_id = random.randrange(len(sprite_files_by_class))
            # pick a random sprite within that class
            sprite_path = random.choice(sprite_files_by_class[class_id])
            sprite_image = Image.open(sprite_path).convert("RGBA")

            # apply any mutations (e.g., color jitter, flips)
            sprite_image = params.apply_mutations(sprite_image, 1)  # one mutation

            # paste it onto the background; paste_sprite returns the updated image
            # plus a YOLO-style annotation line for that one sprite
            background_image, single_annotation = paste_sprite(
                background=background_image,
                sprite=sprite_image,
                class_id=class_id,
            )

            annotations.append(single_annotation)

        # 3) save the final composite
        img_name = f"gen_img_{i:04d}.png"
        background_image.save(os.path.join(save_path, img_name))

        # 4) write out all annotations (one per line)
        annotation_name = f"gen_img_{i:04d}.txt"
        with open(os.path.join(save_path, annotation_name), "w") as f:
            f.write("\n".join(annotations))