import os
from lib.generator import RandomNoiseBackground, RandomNoiseReferenceImageBackground, MutationParameters, generate_dataset
from pathlib import Path

REFERENCE_IMAGES_PATH = Path("img")
BACKGROUND_IMAGES_PATH = Path("img")

DATASET = "pony"

DATASET_SAVE_PATH = Path("img/generated_datasets") / DATASET

SAVE_PATH = DATASET_SAVE_PATH / "sample"

MUTATION_PARAMETERS = MutationParameters(
    background = RandomNoiseReferenceImageBackground(noise = 0.2),
)

os.makedirs(SAVE_PATH, exist_ok=True)

generate_dataset(
    sprites_path = REFERENCE_IMAGES_PATH / DATASET / "sprite",
    backgrounds_path = BACKGROUND_IMAGES_PATH / DATASET / "background",
    save_path = SAVE_PATH,
    count = 1000,
    params = MUTATION_PARAMETERS,
    default_res_x = 1400,
    default_res_y = 1000,
)