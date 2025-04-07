import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from perlin_noise import PerlinNoise

# === 配置 ===
output_dir = "perlin_backgrounds_new"
os.makedirs(output_dir, exist_ok=True)

width, height = 256, 192
num_images = 300
octaves = 4
scale = 0.1
color_1 = (50, 0, 0)       # 暗红
color_2 = (100, 30, 30)    # 大理石红

# === 生成大理石纹理背景 ===
def generate_marble_background(seed: int) -> Image.Image:
    noise = PerlinNoise(octaves=octaves, seed=seed)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    offset_x, offset_y = np.random.uniform(0, 1000), np.random.uniform(0, 1000)

    for y in range(height):
        for x in range(width):
            n = noise([(y * scale) + offset_y, (x * scale) + offset_x])
            n = max(0, min(1, (n + 1) / 2))

            r = int(color_1[0] * (1 - n) + color_2[0] * n)
            g = int(color_1[1] * (1 - n) + color_2[1] * n)
            b = int(color_1[2] * (1 - n) + color_2[2] * n)
            img[y, x] = (r, g, b)

    return Image.fromarray(img, "RGB")

# === 生成血迹遮罩 ===
def generate_blood_mask() -> Image.Image:
    mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    num_blobs = np.random.randint(5, 10)

    for _ in range(num_blobs):
        cx, cy = np.random.randint(0, width), np.random.randint(0, height)
        r = np.random.randint(10, 40)
        color = (150 + np.random.randint(50), 0, 0, 100 + np.random.randint(100))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    return mask.filter(ImageFilter.GaussianBlur(radius=5))

# === 合成函数 ===
def generate_final_image(seed: int) -> Image.Image:
    base = generate_marble_background(seed).convert("RGBA")
    blood = generate_blood_mask()
    return Image.alpha_composite(base, blood)

# === 生成图像 ===
for i in range(num_images):
    seed = np.random.randint(0, 10000)
    final = generate_final_image(seed)
    final.convert("RGB").save(os.path.join(output_dir, f"blood_bg_{i+1:03}.png"))
    print(f"✅ 保存: blood_bg_{i+1:03}.png")

