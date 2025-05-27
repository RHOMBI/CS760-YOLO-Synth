from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
import os
import random
from tqdm import tqdm
import glob


# ========== 设置缓存路径 ==========
os.environ["HF_HOME"] = "E:/huggingface_cache"

# ========== 图像生成参数 ==========
num_images = 200
image_size = (384, 384)
prompt = "top-down pixel-art Isaac-style dungeon room, blood, torches, stone floor"

# ========== 精灵类别路径与编号（请根据实际路径修改）==========
class_dirs = {
    "Player": "E:/760/Player",
    "Tear": "E:/760/Tear",
    "Bullet": "E:/760/Bullet",
    "Poop": "E:/760/Poop",
    "Fly": "E:/760/Fly",
    "Hopper": "E:/760/Hopper",
    "RoundWorm": "E:/760/Round worm",
    "Horf": "E:/760/Horf",
    "Mulligan": "E:/760/Mulligan",
    "Vase": "E:/760/Vase"
}
class_map = {name: idx for idx, name in enumerate(class_dirs)}

# ========== 加载 Sprite 图像（仅从 frames 文件夹递归加载 PNG）==========
sprites_by_class = {}
for class_name, folder in class_dirs.items():
    frame_dir = os.path.join(folder, "frames")
    if not os.path.exists(frame_dir):
        print(f"⚠️ No 'frames' folder for {class_name}, skipping.")
        continue

    sprite_paths = glob.glob(os.path.join(frame_dir, "**", "*.png"), recursive=True)
    sprite_images = []
    for sprite_path in sprite_paths:
        try:
            img = Image.open(sprite_path).convert("RGBA")
            sprite_images.append(img)
        except Exception as e:
            print(f"⚠️ Failed to load {sprite_path}: {e}")

    sprites_by_class[class_name] = sprite_images
    print(f"✅ Loaded {len(sprite_images)} sprites for {class_name}")

# ========== 加载引导图像 ==========
init_image_path = "E:/760/input_images/1.png"
init_image = Image.open(init_image_path).convert("RGB").resize(image_size)

# ========== 初始化 Stable Diffusion Img2Img 模型 ==========
# 初始化 Stable Diffusion 模型
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to("cpu")


# 正确关闭 NSFW 检查器
def dummy_checker(images, clip_input):
    return images, [False] * len(images)

pipe.safety_checker = dummy_checker



# ========== 输出目录 ==========
output_dir = "output"
os.makedirs(f"{output_dir}/images", exist_ok=True)
os.makedirs(f"{output_dir}/labels", exist_ok=True)

# ========== 开始生成图像 ==========
for i in tqdm(range(num_images), desc="生成图像"):
    result = pipe(prompt=prompt, image=init_image, strength=0.6, guidance_scale=7.5).images[0]
    bg = result.convert("RGBA")
    labels = []

    for class_name, class_id in class_map.items():
        candidates = sprites_by_class.get(class_name, [])
        if not candidates:
            continue

        sprite_img = random.choice(candidates)
        scale = random.uniform(0.5, 1.2)
        new_w, new_h = int(sprite_img.width * scale), int(sprite_img.height * scale)
        sprite_resized = sprite_img.resize((new_w, new_h))

        x = random.randint(0, image_size[0] - new_w)
        y = random.randint(0, image_size[1] - new_h)
        bg.paste(sprite_resized, (x, y), sprite_resized)

        cx = (x + new_w / 2) / image_size[0]
        cy = (y + new_h / 2) / image_size[1]
        w = new_w / image_size[0]
        h = new_h / image_size[1]
        labels.append(f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    # 保存图像和标签
    img_name = f"image_{i:03d}.jpg"
    label_name = f"image_{i:03d}.txt"
    bg.convert("RGB").save(f"{output_dir}/images/{img_name}")
    with open(f"{output_dir}/labels/{label_name}", "w") as f:
        f.write("\n".join(labels))

print("\n✅ 所有图像与 YOLO 标签已成功生成！")


