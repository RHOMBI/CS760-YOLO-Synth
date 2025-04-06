import os
import random
from PIL import Image, ImageEnhance, ImageFilter

AUG_PER_TYPE = 3

# Enter the path to the original image
sprites_dir = "sprites"

# Individual augmentation function definitions (with randomization)
def apply_rotate(img):
    angle = random.randint(-45, 45)
    return img.rotate(angle, expand=True)

def apply_scale(img):
    scale = random.uniform(0.7, 1.3)
    w, h = img.size
    return img.resize((int(w * scale), int(h * scale)))

def apply_flip(img):
    return img.transpose(random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM]))

def apply_brightness(img):
    factor = random.uniform(0.7, 1.5)
    return ImageEnhance.Brightness(img).enhance(factor)

def apply_contrast(img):
    factor = random.uniform(0.7, 1.5)
    return ImageEnhance.Contrast(img).enhance(factor)

def apply_sharpen(img):
    factor = random.uniform(1.5, 3.0)
    return ImageEnhance.Sharpness(img).enhance(factor)

def apply_blur(img):
    radius = random.uniform(0.5, 2.5)
    return img.filter(ImageFilter.GaussianBlur(radius))

# Enhanced operation mapping
augmentation_ops = {
    "rotate": apply_rotate,
    "scale": apply_scale,
    "flip": apply_flip,
    "brightness": apply_brightness,
    "contrast": apply_contrast,
    "sharpen": apply_sharpen,
    "blur": apply_blur
}

# Iterate over the original image
for fname in os.listdir(sprites_dir):
    if not fname.lower().endswith((".png", ".jpg", ".webp")):
        continue

    input_path = os.path.join(sprites_dir, fname)
    base_name = os.path.splitext(fname)[0]
    output_dir = os.path.join(sprites_dir, base_name)
    os.makedirs(output_dir, exist_ok=True)

    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f" 无法打开图像 {fname}: {e}")
        continue

    # 每种操作执行多次随机变换
    for aug_name, func in augmentation_ops.items():
        for i in range(AUG_PER_TYPE):
            aug_img = func(img)
            out_path = os.path.join(output_dir, f"aug_{aug_name}_{i}.png")
            aug_img.save(out_path)
            print(f" {out_path}")
