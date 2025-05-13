import os
import cv2
from ultralytics import YOLO

from pathlib import Path

TEST_PATH = Path("test")
PRED_PATH = Path("predictions")

os.makedirs(TEST_PATH, exist_ok=True)
os.makedirs(PRED_PATH, exist_ok=True)

model = YOLO("runs/detect/train/weights/best.pt")

example_image = None

for image_path in TEST_PATH.glob("*.jpg"):
    image = cv2.imread(str(image_path))

    print(image_path.stem)
    if example_image is None:
        example_image = image.copy()

    results = model.predict(source=image, conf=0.3, verbose=False)

    r = results[0]

    boxes = r.boxes.xyxy.cpu().numpy()
    confs = r.boxes.conf.cpu().numpy()
    classes = r.boxes.cls.cpu().numpy().astype(int)

    pred_file = PRED_PATH / f"{image_path.stem}.txt"
    with open(pred_file, "w") as f:
        for cls, conf, (x1, y1, x2, y2) in zip(classes, confs, boxes):
            x1 /= image.shape[1]
            y1 /= image.shape[0]
            x2 /= image.shape[1]
            y2 /= image.shape[0]

            f.write(f"{cls} {conf:.4f} {x1} {y1} {x2} {y2}\n")

cv2.waitKey(0)
cv2.destroyAllWindows()
