import os

from PIL import Image
from typing import Dict, List
from pathlib import Path

import random
import math

from typing import Dict, List, Tuple

from lib.annotate import paste_sprite, paste_sprite_at

CLASS_COUNT = 10

REFERENCE_ANNOTATIONS_PATH = Path("datasets") / "isaac_real"
CLASSES_PATH = Path("img") / "isaac"

REFERENCE_IMAGES_PATH = Path("img")
BACKGROUND_IMAGES_PATH = Path("img")

DATASET = "isaac"
DATASET_SAVE_PATH = Path("datasets") / "yards_dataset"


SAVE_PATH = DATASET_SAVE_PATH / "sample"

os.makedirs(SAVE_PATH, exist_ok=True)

frequency_space: Dict[int, List[int]] = {i: [] for i in range(CLASS_COUNT)}
classes: List[str] = []
position_samplers: Dict[int, "PositionSampler"] = {}

def load_classes(dataset_path: Path):
    label_file = dataset_path / "classes.txt"
    with label_file.open("r") as f:
        for line in f:
            cls = line.strip()
            if cls:
                classes.append(cls)

def calculate_frequency_space(dataset_path: Path):

   for label_file in dataset_path.glob("*.txt"):
      with label_file.open("r") as f:
         
        frequency: Dict[int, int] = {i: 0 for i in range(CLASS_COUNT)}
        for line in f:
            line = line.strip()
            if not line:
               continue
            obj_class = line.split(None, 1)[0]
            try:
               obj_class = int(obj_class)
            except:
               continue
            frequency[obj_class] += 1
        
        for obj_class in range(0, CLASS_COUNT):
            frequency_space[obj_class].append(frequency[obj_class])

def load_observed_positions(
    labels_dir: Path,
    class_id: int
) -> List[Tuple[float,float]]:
    """Return all normalized (x_center, y_center) for the given class."""
    coords: List[Tuple[float,float]] = []
    for txt in labels_dir.glob("*.txt"):
        for line in txt.open():
            parts = line.strip().split()
            if not parts:
                continue
            c = int(parts[0])
            if c != class_id:
                continue
            # YOLO format: class x_center y_center width height
            x, y = float(parts[1]), float(parts[2])
            coords.append((x, y))
    if not coords:
        raise RuntimeError(f"No annotations found for class {class_id}")
    return coords

class PositionSampler:
    """Mixture of 2D Epanechnikov (parabolic) kernels over observed points."""
    def __init__(self, coords: List[Tuple[float,float]], kernel_radius: float = 0.05):
        self.coords = coords
        self.h = kernel_radius

    def sample(self) -> Tuple[float,float]:
        # 1) pick one observed center
        x0, y0 = random.choice(self.coords)

        # 2) sample radial distance r from inverted CDF of the parabolic kernel
        u = random.random()
        r = self.h * math.sqrt(1 - math.sqrt(1 - u))

        # 3) pick a random angle
        theta = random.random() * 2 * math.pi
        dx = r * math.cos(theta)
        dy = r * math.sin(theta)

        # 4) clamp to [0,1]
        x = min(max(x0 + dx, 0.0), 1.0)
        y = min(max(y0 + dy, 0.0), 1.0)
        return x, y

def build_all_samplers():
    """Instantiate a PositionSampler for each class and store it globally."""
    for cls in range(CLASS_COUNT):
        coords = load_observed_positions(REFERENCE_ANNOTATIONS_PATH, cls)
        # you can tweak kernel_radius per class if you like
        position_samplers[cls] = PositionSampler(coords, kernel_radius=0.05)

def get_sampled_coordinates(class_id: int) -> Tuple[float,float]:
    """Draw one (x,y) from the learned PDF for this class."""
    sampler = position_samplers.get(class_id)
    if sampler is None:
        raise RuntimeError(f"Sampler for class {class_id} not built yet.")
    return sampler.sample()


def generate_dataset(
        sprites_path: Path,
        backgrounds_path: Path,
        save_path: Path,
        count: int,
        train: float = 0.8,
):
   backgrounds = []
   for f in backgrounds_path.iterdir():
      if f.suffix.lower() in ('.png', '.jpg', '.jpeg'):
         img = Image.open(f)
         backgrounds.append(img)

   sprites_per_class = [[] for _ in range(CLASS_COUNT)]
   for i, cls in enumerate(classes):
      class_dir = sprites_path / cls
      for f in class_dir.iterdir():
         if f.suffix.lower() in ('.png', '.jpg', '.jpeg'):
               sprites_per_class[i].append(Image.open(f))
   
   folder = "train"
   for i in range(0, count):
      if i > train * count:
         folder = "val"

      print(f"Generating image {i + 1}/{count}...")
      background_image = random.choice(backgrounds).copy()
      annotations = []
      for (class_id, sprite_files) in enumerate(sprites_per_class):
         paste_count = random.choice(frequency_space[class_id])

         for j in range(paste_count):
            sprite_image = random.choice(sprite_files)

            x_norm, y_norm = get_sampled_coordinates(class_id)
            print(f"  Pasting sprite {j + 1}/{paste_count} of class {class_id} at ({x_norm:.2f}, {y_norm:.2f})")
            background_image, ann = paste_sprite_at(background=background_image, sprite=sprite_image, x=x_norm, y=y_norm, class_id=class_id)
            annotations.append(ann)

      img_name = f"gen_img_{i:04d}.png"

      img_dir = os.path.join(save_path, "images", folder)
      os.makedirs(img_dir, exist_ok=True)
      labels_dir = os.path.join(save_path, "labels", folder)
      os.makedirs(labels_dir, exist_ok=True)

      background_image.save(os.path.join(img_dir, img_name))

      annotation_name = f"gen_img_{i:04d}.txt"
      with open(os.path.join(labels_dir, annotation_name), "w+") as f:
         f.write("\n".join(annotations))

load_classes(CLASSES_PATH)
calculate_frequency_space(REFERENCE_ANNOTATIONS_PATH)
build_all_samplers()

generate_dataset(
   sprites_path = REFERENCE_IMAGES_PATH / DATASET / "sprite",
   backgrounds_path = BACKGROUND_IMAGES_PATH / DATASET / "background",
   save_path = SAVE_PATH,
   count = 1000,
)

