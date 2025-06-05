import os
import shutil
import random

# ─── Configuration ─────────────────────────────────────────────────────────────
background_folders = ['desert', 'forest', 'ice', 'lava']
labels_folder_src   = 'labels_original'
output_base         = '.'
train_ratio         = 0.8
random_seed         = 42

# ─── Setup ─────────────────────────────────────────────────────────────────────
random.seed(random_seed)

# Create target directories
for data_type in ['images', 'labels']:
    for split in ['train', 'val']:
        os.makedirs(os.path.join(output_base, data_type, split), exist_ok=True)

# ─── Gather all (image, label) pairs ────────────────────────────────────────────
pairs = []
for folder in background_folders:
    folder_path = os.path.join(output_base, folder)
    if not os.path.isdir(folder_path):
        print(f"Warning: background folder '{folder}' not found, skipping.")
        continue
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            name, ext = os.path.splitext(fname)
            new_base = f"{folder}_{name}"
            img_src   = os.path.join(folder_path, fname)
            lbl_src   = os.path.join(output_base, labels_folder_src, f"{name}.txt")
            if os.path.exists(lbl_src):
                pairs.append((img_src, lbl_src, new_base, ext))
            else:
                print(f"Warning: Label missing for '{fname}' in '{labels_folder_src}'")

# ─── Shuffle & split ────────────────────────────────────────────────────────────
random.shuffle(pairs)
split_idx    = int(len(pairs) * train_ratio)
train_pairs  = pairs[:split_idx]
val_pairs    = pairs[split_idx:]

# ─── Copy function ──────────────────────────────────────────────────────────────
def copy_set(pairs_list, split_name):
    for img_src, lbl_src, new_base, ext in pairs_list:
        img_dst = os.path.join(output_base, 'images', split_name, new_base + ext)
        lbl_dst = os.path.join(output_base, 'labels', split_name, new_base + '.txt')
        shutil.copy2(img_src, img_dst)
        shutil.copy2(lbl_src, lbl_dst)

# ─── Execute copy ───────────────────────────────────────────────────────────────
copy_set(train_pairs, 'train')
copy_set(val_pairs,   'val')

print(f"Done! {len(train_pairs)} training and {len(val_pairs)} validation samples created.")
