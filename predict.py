import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")

results = model.predict(source="test/pony/img3.png", show=True, conf=0.75)

cv2.waitKey(0)
cv2.destroyAllWindows()
