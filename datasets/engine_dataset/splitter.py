import random
import shutil
from pathlib import Path

def split_dataset(images_dir: str, labels_dir: str, train_ratio: float = 0.8):
    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)

    # 1) Gather all image files (adjust extensions as needed)
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    image_files = [f for f in images_dir.iterdir() 
                   if f.is_file() and f.suffix.lower() in exts]

    # 2) Shuffle and split
    random.shuffle(image_files)
    split_idx = int(len(image_files) * train_ratio)
    train_images = image_files[:split_idx]
    val_images   = image_files[split_idx:]

    # 3) Create train/val subdirs
    for subset in ('train', 'val'):
        (images_dir / subset).mkdir(exist_ok=True)
        (labels_dir / subset).mkdir(exist_ok=True)

    # 4) Move files
    def move_pair(img_list, subset):
        for img_path in img_list:
            # move image
            dest_img = images_dir / subset / img_path.name
            shutil.move(str(img_path), dest_img)

            # move corresponding label
            label_path = labels_dir / f"{img_path.stem}.txt"
            if label_path.exists():
                dest_lbl = labels_dir / subset / label_path.name
                shutil.move(str(label_path), dest_lbl)
            else:
                print(f"⚠️  Warning: no label for {img_path.name}")

    move_pair(train_images, 'train')
    move_pair(val_images,   'val')

if __name__ == "__main__":
    split_dataset('images', 'labels', train_ratio=0.8)
