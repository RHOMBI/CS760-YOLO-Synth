import os

from PIL import Image
from typing import Dict, List
from pathlib import Path

import random

from lib.annotate import paste_sprite

CLASS_COUNT = 4

REFERENCE_ANNOTATIONS_PATH = Path("datasets") / "isaac_real" / "labels" / "train"
CLASSES_PATH = Path("datasets") / "isaac_real"

REFERENCE_IMAGES_PATH = Path("img")
BACKGROUND_IMAGES_PATH = Path("img")

DATASET = "isaac"
DATASET_SAVE_PATH = Path("datasets") / DATASET / "yards"


SAVE_PATH = DATASET_SAVE_PATH / "sample"

os.makedirs(SAVE_PATH, exist_ok=True)

frequency_space: Dict[int, List[int]] = {i: [] for i in range(CLASS_COUNT)}
classes: List[str] = []

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

            background_image, ann = paste_sprite(background=background_image, sprite=sprite_image, class_id=class_id)
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

generate_dataset(
   sprites_path = REFERENCE_IMAGES_PATH / DATASET / "sprite",
   backgrounds_path = BACKGROUND_IMAGES_PATH / DATASET / "background",
   save_path = SAVE_PATH,
   count = 1000,
)

