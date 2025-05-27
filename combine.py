import os
from PIL import Image

def combine_head_with_bodies(
    head_path: str,
    body_folder: str,
    output_prefix: str,
    output_folder: str,
    final_height: int = 36,
    overlap: int = 2,
    body_x_offset: int = 1  # 根据你测试的偏移量
):
    """
    Stitch a head image with multiple body images, output named output_prefix_serial number.png

    :param head_path: path of head image
    :param body_folder: path to body image folder
    :param output_prefix: output filename prefix (e.g. "isaac_down")
    :param output_folder: output folder path
    :param final_height: final image height
    :param overlap: number of pixels where the head overlaps the body
    :param body_x_offset: body horizontal trim offset

    """
    os.makedirs(output_folder, exist_ok=True)

    head = Image.open(head_path)
    body_files = sorted([f for f in os.listdir(body_folder) if f.endswith(".png")])

    for i, body_file in enumerate(body_files):
        body = Image.open(os.path.join(body_folder, body_file))

        final_width = max(head.width, body.width)
        head_x = (final_width - head.width) // 2
        body_x = (final_width - body.width) // 2 + body_x_offset
        body_y = head.height - overlap - 3

        combined = Image.new("RGBA", (final_width, final_height), (0, 0, 0, 0))
        combined.paste(body, (body_x, body_y), body)
        combined.paste(head, (head_x, 0), head)

        output_path = os.path.join(output_folder, f"{output_prefix}_{i}.png")
        combined.save(output_path)



## Isaac character sprite generation
# Isaac walk down open eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_0.png",
    body_folder="img/origin/Isaac/body-down",
    output_prefix="Isaac_down0",
    output_folder="img/origin/Isaac/output"
)
# Isaac walk down close eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_1.png",
    body_folder="img/origin/Isaac/body-down",
    output_prefix="Isaac_down1",
    output_folder="img/origin/Isaac/output"
)
# Isaac walk up open eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_4.png",
    body_folder="img/origin/Isaac/body-up",
    output_prefix="Isaac_up0",
    output_folder="img/origin/Isaac/output",
    body_x_offset=-1
)
# Isaac walk up close eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_5.png",
    body_folder="img/origin/Isaac/body-up",
    output_prefix="Isaac_up1",
    output_folder="img/origin/Isaac/output",
    body_x_offset=-1
)
# Isaac walk right open eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_2.png",
    body_folder="img/origin/Isaac/body-right",
    output_prefix="Isaac_right0",
    output_folder="img/origin/Isaac/output"
)
# Isaac walk right close eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_3.png",
    body_folder="img/origin/Isaac/body-right",
    output_prefix="Isaac_right1",
    output_folder="img/origin/Isaac/output"
)
# Isaac walk left open eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_6.png",
    body_folder="img/origin/Isaac/body-left",
    output_prefix="Isaac_left0",
    output_folder="img/origin/Isaac/output",
    body_x_offset=-1
)
# Isaac walk left close eyes
combine_head_with_bodies(
    head_path="img/origin/Isaac/head/head_7.png",
    body_folder="img/origin/Isaac/body-left",
    output_prefix="Isaac_left1",
    output_folder="img/origin/Isaac/output",
    body_x_offset=-1
)
## Isaac character sprite generation end

## Cain character sprite generation
# Cain walk down open eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_0.png",
    body_folder="img/origin/Cain/body-down",
    output_prefix="Cain_down0",
    output_folder="img/origin/Cain/output"
)
# Cain walk down close eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_1.png",
    body_folder="img/origin/Cain/body-down",
    output_prefix="Cain_down1",
    output_folder="img/origin/Cain/output"
)
# Cain walk up open eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_4.png",
    body_folder="img/origin/Cain/body-up",
    output_prefix="Cain_up0",
    output_folder="img/origin/Cain/output",
    body_x_offset=-1
)
# Cain walk up close eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_5.png",
    body_folder="img/origin/Cain/body-up",
    output_prefix="Cain_up1",
    output_folder="img/origin/Cain/output",
    body_x_offset=-1
)
# Cain walk right open eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_2.png",
    body_folder="img/origin/Cain/body-right",
    output_prefix="Cain_right0",
    output_folder="img/origin/Cain/output"
)
# Cain walk right close eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_3.png",
    body_folder="img/origin/Cain/body-right",
    output_prefix="Cain_right1",
    output_folder="img/origin/Cain/output"
)
# Cain walk left open eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_6.png",
    body_folder="img/origin/Cain/body-left",
    output_prefix="Cain_left0",
    output_folder="img/origin/Cain/output",
    body_x_offset=-1
)
# Cain walk left close eyes
combine_head_with_bodies(
    head_path="img/origin/Cain/head/head_7.png",
    body_folder="img/origin/Cain/body-left",
    output_prefix="Cain_left1",
    output_folder="img/origin/Cain/output",
    body_x_offset=-1
)
## Cain character sprite generation end

## Magdalene character sprite generation
# Magdalene walk down open eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_0.png",
    body_folder="img/origin/Magdalene/body-down",
    output_prefix="Magdalene_down0",
    output_folder="img/origin/Magdalene/output",
    final_height=40,  # Magdalene's body is slightly taller
    overlap=2,  # Adjust overlap for Magdalene
    body_x_offset=2  # Adjust horizontal offset for Magdalene
)
# Magdalene walk down close eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_1.png",
    body_folder="img/origin/Magdalene/body-down",
    output_prefix="Magdalene_down1",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=2
)
# Magdalene walk up open eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_4.png",
    body_folder="img/origin/Magdalene/body-up",
    output_prefix="Magdalene_up0",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=0
)
# Magdalene walk up close eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_5.png",
    body_folder="img/origin/Magdalene/body-up",
    output_prefix="Magdalene_up1",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=0
)
# Magdalene walk right open eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_2.png",
    body_folder="img/origin/Magdalene/body-right",
    output_prefix="Magdalene_right0",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=2
)
# Magdalene walk right close eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_3.png",
    body_folder="img/origin/Magdalene/body-right",
    output_prefix="Magdalene_right1",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=2
)
# Magdalene walk left open eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_6.png",
    body_folder="img/origin/Magdalene/body-left",
    output_prefix="Magdalene_left0",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=0
)
# Magdalene walk left close eyes
combine_head_with_bodies(
    head_path="img/origin/Magdalene/head/head_7.png",
    body_folder="img/origin/Magdalene/body-left",
    output_prefix="Magdalene_left1",
    output_folder="img/origin/Magdalene/output",
    final_height=40,
    overlap=2,
    body_x_offset=0
)
## Magdalene character sprite generation end

## Mulligan character sprite generation
combine_head_with_bodies(
    head_path="img/origin/Mulligan/head/head_0.png",
    body_folder="img/origin/Mulligan/body",
    output_prefix="Mulligan0",
    output_folder="img/origin/Mulligan/output",
    final_height=37,
    overlap=8,
    body_x_offset=0
)
combine_head_with_bodies(
    head_path="img/origin/Mulligan/head/head_1.png",
    body_folder="img/origin/Mulligan/body",
    output_prefix="Mulligan1",
    output_folder="img/origin/Mulligan/output",
    final_height=37,
    overlap=8,
    body_x_offset=0
)
combine_head_with_bodies(
    head_path="img/origin/Mulligan/head/head_2.png",
    body_folder="img/origin/Mulligan/body",
    output_prefix="Mulligan2",
    output_folder="img/origin/Mulligan/output",
    final_height=37,
    overlap=8,
    body_x_offset=0
)
combine_head_with_bodies(
    head_path="img/origin/Mulligan/head/head_3.png",
    body_folder="img/origin/Mulligan/body",
    output_prefix="Mulligan3",
    output_folder="img/origin/Mulligan/output",
    final_height=37,
    overlap=8,
    body_x_offset=0
)
combine_head_with_bodies(
    head_path="img/origin/Mulligan/head/head_4.png",
    body_folder="img/origin/Mulligan/body",
    output_prefix="Mulligan4",
    output_folder="img/origin/Mulligan/output",
    final_height=37,
    overlap=8,
    body_x_offset=0
)
combine_head_with_bodies(
    head_path="img/origin/Mulligan/head/head_5.png",
    body_folder="img/origin/Mulligan/body",
    output_prefix="Mulligan5",
    output_folder="img/origin/Mulligan/output",
    final_height=37,
    overlap=8,
    body_x_offset=0
)
