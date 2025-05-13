#this file is used to convert the annotation format from
# class x_centroid y_centroid width height
# to
# class x1 y1 x2 y2

from pathlib import Path


input_dir = Path("mAP-master/input/ground-truth")
output_dir = input_dir.parent / "annotations_xyxy"
output_dir.mkdir(exist_ok=True)

for txt_file in input_dir.glob("*.txt"):
    new_lines = []
    with txt_file.open() as f:
        for line in f:
            cls, xc, yc, w, h = line.split()
            xc, yc, w, h = map(float, (xc, yc, w, h))
            x1 = xc - w/2
            y1 = yc - h/2
            x2 = xc + w/2
            y2 = yc + h/2
            new_lines.append(f"{cls} {x1} {y1} {x2} {y2}\n")

    out_path = output_dir / txt_file.name
    with out_path.open("w") as f_out:
        f_out.writelines(new_lines)
