from lib.generator import RandomNoiseBackground, RandomNoiseReferenceImageBackground, MutationParameters, generate_dataset
from pathlib import Path

REFERENCE_IMAGE_PATH = Path("reference_images")
DATASET_SAVE_PATH = Path("generated_datasets")

REFERENCE_IMAGES = [
    REFERENCE_IMAGE_PATH / "sprites" / "isaac.png"
]

REFERENCE_BACKGROUNDS = [
    REFERENCE_IMAGE_PATH / "backgrounds" / "room1.webp"
]

SAVE_PATH = DATASET_SAVE_PATH / "1"

MUTATION_PARAMETERS = MutationParameters(
    background = RandomNoiseReferenceImageBackground(reference_paths = REFERENCE_BACKGROUNDS, noise = 0.5),
)

generate_dataset(
    asset_paths = REFERENCE_IMAGES,
    save_path = SAVE_PATH,
    count = 5,
    params = MUTATION_PARAMETERS,
    res_x = 1000,
    res_y = 1000,
)