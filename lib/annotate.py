import os
import random
from PIL import Image

# Helper function: paste sprite onto the background and return annotation
def paste_sprite(background, sprite, class_id=0):
    bg_width, bg_height = background.size
    sprite_width, sprite_height = sprite.size

    # Random position
    max_x = bg_width - sprite_width
    max_y = bg_height - sprite_height

    x = random.randint(0, max(0, max_x))
    y = random.randint(0, max(0, max_y))

    background.paste(sprite, (x, y), sprite if sprite.mode == 'RGBA' else None)

    # Calculate YOLO formatted coordinates
    center_x = (x + sprite_width / 2) / bg_width
    center_y = (y + sprite_height / 2) / bg_height
    rel_width = sprite_width / bg_width
    rel_height = sprite_height / bg_height

    annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {rel_width:.6f} {rel_height:.6f}"
    return background, annotation
