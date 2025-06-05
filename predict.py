import os
import cv2
from ultralytics import YOLO
from pathlib import Path
import argparse   # ← new

# 1) set up argparse
parser = argparse.ArgumentParser(
    description="Run YOLO inference and dump predictions",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "-m", "--model-path",
    type=str,
    default="runs_diffusion/train/weights/best.pt",
    help="path to the .pt weights file"
)  # default is your current hard-coded path :contentReference[oaicite:0]{index=0}

args = parser.parse_args()

# 2) use the CLI value instead of the literal string
model = YOLO(args.model_path)

# rest of your code unchanged
TEST_PATH = Path("test/images")
PRED_PATH = Path("mAP-master") / "input" / "detection-results"

os.makedirs(TEST_PATH, exist_ok=True)
os.makedirs(PRED_PATH, exist_ok=True)

example_image = None
for image_path in TEST_PATH.glob("*.png"):
    image = cv2.imread(str(image_path))
    # print(image_path.stem)
    if example_image is None:
        example_image = image.copy()

    results = model.predict(source=image, conf=0.1, verbose=False)
    r = results[0]

    boxes = r.boxes.xyxy.cpu().numpy()
    confs = r.boxes.conf.cpu().numpy()
    classes = r.boxes.cls.cpu().numpy().astype(int)

    with open(PRED_PATH / f"{image_path.stem}.txt", "w") as f:
        for cls, conf, (x1, y1, x2, y2) in zip(classes, confs, boxes):
            # normalize
            h, w = image.shape[:2]
            x1, x2 = x1/w, x2/w
            y1, y2 = y1/h, y2/h
            f.write(f"{cls} {conf:.4f} {x1} {y1} {x2} {y2}\n")

cv2.waitKey(1)
cv2.destroyAllWindows()
