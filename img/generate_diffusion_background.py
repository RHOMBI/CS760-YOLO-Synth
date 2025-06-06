import os
import torch

# ========== Monkey-patch for PyTorch 2.8+ ==========
# In PyTorch 2.8+, `_cuda_endAllocateCurrentStreamToPool` was removed.
# Create an alias to `_cuda_endAllocateToPool` if needed.
try:
    # Attempt to access the symbol; if missing, this will raise ImportError
    getattr(torch._C, "_cuda_endAllocateCurrentStreamToPool")
except (AttributeError, ImportError):
    # Alias it to the existing implementation `_cuda_endAllocateToPool`
    # so that torch.cuda.memory code will not crash.
    torch._C._cuda_endAllocateCurrentStreamToPool = torch._C._cuda_endAllocateToPool

# ========== 继续原有脚本 ==========
from diffusers import StableDiffusionImg2ImgPipeline  # Now safe to import :contentReference[oaicite:11]{index=11}
from PIL import Image
import random
from tqdm import tqdm
import glob

# ========== 设置缓存路径 ==========
os.environ["HF_HOME"] = "E:/huggingface_cache"

# ========== 图像生成参数 ==========
num_images = 1000
image_size = (390, 234)
prompt = "top-down pixel-art Isaac-style dungeon room, blood, torches, stone floor"

# ========== 精灵类别路径与编号（请根据实际路径修改）==========
class_dirs = {
    "Player": "sprite/0_Player",
    "Tear": "sprite/1_Tear",
    "Bullet": "sprite/2_Bullet",
    "Poop": "sprite/3_Poop",
    "Fly": "sprite/4_Fly",
    "Hopper": "sprite/5_Hopper",
    "RoundWorm": "sprite/6_Round worm",
    "Horf": "sprite/7_Horf",
    "Mulligan": "sprite/8_Mulligan",
    "Vase": "sprite/9_Vase"
}
class_map = {name: idx for idx, name in enumerate(class_dirs)}

# ========== 加载 Sprite 图像（仅从 frames 文件夹递归加载 PNG）==========
sprites_by_class = {}
for class_name, folder in class_dirs.items():
    #frame_dir = os.path.join(folder, "frames")
    frame_dir = folder
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
init_image_path = "sprite/input_images/1.png"
init_image = Image.open(init_image_path).convert("RGB").resize(image_size)

# ========== 初始化 Stable Diffusion Img2Img 模型 ==========
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to("cuda")  # “gpu” 和 “cuda” 等价，确保 GPU 上下文正确 :contentReference[oaicite:12]{index=12}

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
