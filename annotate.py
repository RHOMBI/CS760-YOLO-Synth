import os
import random
from PIL import Image

# Create the output directory
os.makedirs('img/generate_img', exist_ok=True)

# Helper function: paste sprite onto the background and return annotation
# def paste_sprite(background, sprite, class_id=0):
#     bg_width, bg_height = background.size
#     sprite_width, sprite_height = sprite.size
#
#     # Random position
#     max_x = bg_width - sprite_width
#     max_y = bg_height - sprite_height
#
#     x = random.randint(0, max(0, max_x))
#     y = random.randint(0, max(0, max_y))
#
#     background.paste(sprite, (x, y), sprite if sprite.mode == 'RGBA' else None)
#
#
#     center_x = (x + sprite_width / 2) / bg_width
#     center_y = (y + sprite_height / 2) / bg_height
#     rel_width = sprite_width / bg_width
#     rel_height = sprite_height / bg_height
#
#     annotation = f"{class_id} {center_x:.6f} {center_y:.6f} {rel_width:.6f} {rel_height:.6f}"
#     return background, annotation

def paste_sprite(background, sprite, position, class_id):
    bg_width, bg_height = background.size
    sprite_width, sprite_height = sprite.size

    background.paste(sprite, position, sprite if sprite.mode == 'RGBA' else None)

    # Calculate YOLO formatted coordinates
    center_x = (position[0] + sprite_width / 2) / bg_width
    center_y = (position[1] + sprite_height / 2) / bg_height
    rel_width = sprite_width / bg_width
    rel_height = sprite_height / bg_height

    return f"{class_id} {center_x:.6f} {center_y:.6f} {rel_width:.6f} {rel_height:.6f}"

# Helper function: check the sprite for overlap
def is_overlap(pos, size, positions):
    x1, y1 = pos
    w1, h1 = size
    for (x2, y2), (w2, h2) in positions:
        if not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1):# overlap, no more space for sprite
            return True
    return False

# Helper function: generate random position
def random_position(bg_size, sprite_size, positions, margin=45, max_attempts=100):
    bg_width, bg_height = bg_size
    sprite_width, sprite_height = sprite_size

    max_x = bg_width - sprite_width - margin
    max_y = bg_height - sprite_height - margin
    min_x, min_y = margin, margin

    # Check if the sprite can fit in the background(enough space)
    for _ in range(max_attempts):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        if not is_overlap((x, y), sprite_size, positions):
            return (x, y)
    raise ValueError("Cannot find non-overlapping position.")

# Main function
def generate_dataset(num_images):
    background_folder = 'img/background'
    sprite_base_folder = 'img/sprite'

    background_files = [os.path.join(background_folder, f) for f in os.listdir(background_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

    for i in range(1, num_images + 1):
        # Randomly select the sprite folders and their maximum counts
        sprite_folders = {
            'player': {'path': os.path.join(sprite_base_folder, 'player'), 'max': 1, 'class_id': 0},
            'bullet': {'path': os.path.join(sprite_base_folder, 'bullet'), 'max': random.randint(0, 3), 'class_id': 1},
            'enemy': {'path': os.path.join(sprite_base_folder, 'enemy'), 'max': random.randint(0, 3), 'class_id': 2},
            'item': {'path': os.path.join(sprite_base_folder, 'items'), 'max': random.randint(0, 1), 'class_id': 3},
        }

        background_path = random.choice(background_files)
        background_img = Image.open(background_path).convert("RGBA")
        annotations = []
        placed_positions = []

        for sprite_type, sprite_info in sprite_folders.items():
            sprite_files = [os.path.join(sprite_info['path'], f) for f in os.listdir(sprite_info['path']) if f.endswith(('png', 'jpg', 'jpeg'))]
            count = sprite_info['max']

            for _ in range(count):
                sprite_path = random.choice(sprite_files)
                sprite_img = Image.open(sprite_path).convert("RGBA")
                sprite_size = sprite_img.size

                try:
                    position = random_position(background_img.size, sprite_size, placed_positions, margin=50)
                    placed_positions.append((position, sprite_size))
                    annotation = paste_sprite(background_img, sprite_img, position, sprite_info['class_id'])
                    annotations.append(annotation)
                except ValueError:
                    print(f"Warning: Could not place {sprite_type} without overlap after multiple attempts.")

        # save the image
        img_name = f"gen_img_{i:04d}.png"
        background_img.save(os.path.join('img/generate_img', img_name))

        # save the annotations
        annotation_name = f"gen_img_{i:04d}.txt"
        with open(os.path.join('img/generate_img', annotation_name), "w") as f:
            f.write("\n".join(annotations))

# Example usage
generate_dataset(100)
