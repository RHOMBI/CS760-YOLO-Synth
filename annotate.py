import os
import random
from PIL import Image

# Create the output directory
os.makedirs('img/generate_img', exist_ok=True)

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

# Main function
def generate_dataset(num_images):
    sprite_folder = 'img/sprite'
    background_folder = 'img/background'

    sprite_files = [os.path.join(sprite_folder, f) for f in os.listdir(sprite_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
    background_files = [os.path.join(background_folder, f) for f in os.listdir(background_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

    for i in range(1, num_images + 1):
        sprite_path = random.choice(sprite_files)
        background_path = random.choice(background_files)

        sprite_img = Image.open(sprite_path).convert("RGBA")
        background_img = Image.open(background_path).convert("RGBA")

        generated_img, annotation = paste_sprite(background_img, sprite_img)

        # Save generated image
        img_name = f"gen_img_{i:04d}.png"
        generated_img.save(os.path.join('img/generate_img', img_name))

        # Save annotation
        annotation_name = f"gen_img_{i:04d}.txt"
        with open(os.path.join('img/generate_img', annotation_name), "w") as f:
            f.write(annotation)

# Example usage
generate_dataset(5)
