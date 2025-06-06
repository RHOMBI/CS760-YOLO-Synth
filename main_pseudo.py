from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import random

# === 参数配置 ===
style_root = Path("styles")
image_root = Path("yolo/images")  # 你的新截图目录
output_root = Path("pseudo_results_radial")
output_root.mkdir(exist_ok=True)

valid_exts = [".png", ".jpg", ".jpeg"]

# === 创建径向透明度遮罩（你原来的方式） ===
def generate_radial_mask(size):
    """生成中心透明度为1，边缘为0的径向alpha遮罩（线性叠加 + 模糊）"""
    width, height = size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)

    max_radius = int((width**2 + height**2) ** 0.5 / 2)
    for r in range(max_radius, 0, -10):
        alpha = int(255 * (r / max_radius))  # 线性从255到0
        draw.ellipse(
            [(width // 2 - r, height // 2 - r), (width // 2 + r, height // 2 + r)],
            fill=alpha
        )
    return mask.filter(ImageFilter.GaussianBlur(20))

# === 主逻辑 ===
for style_dir in style_root.iterdir():
    if not style_dir.is_dir():
        continue

    style_name = style_dir.name.replace("isaac2", "")
    style_images = [img for img in style_dir.glob("*") if img.suffix.lower() in valid_exts]
    if not style_images:
        print(f"⚠ 空风格目录：{style_dir}")
        continue

    output_dir = output_root / style_name
    output_dir.mkdir(parents=True, exist_ok=True)

    for img_path in image_root.glob("*.png"):
        if img_path.suffix.lower() not in valid_exts:
            continue
        try:
            base_img = Image.open(img_path).convert("RGBA")
            style_img = Image.open(random.choice(style_images)).convert("RGBA").resize(base_img.size)

            mask = generate_radial_mask(base_img.size)
            blended = Image.composite(style_img, base_img, mask)

            output_path = output_dir / img_path.with_suffix(".png").name
            blended.save(output_path)
            print(f"✅ 保存：{output_path}")
        except Exception as e:
            print(f"❌ 错误处理 {img_path}: {e}")

print("\n🎯 所有带径向透明度的伪风格迁移图已生成：pseudo_results_radial/")