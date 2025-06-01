import cv2
from matplotlib import pyplot as plt
from augmentation import apply_augmentation
from ocr import get_text
from plate_extract import preprocess

img = cv2.imread("car1.jpg")
img = apply_augmentation(img)
canny, output_img, plate_coord = preprocess(img.copy())
plate_img = None
if plate_coord is not None:
    x, y, w, h = plate_coord
    plate_img = img[y:y + h, x:x + w]
    plate_text = get_text(plate_img)
    print(plate_text)
    cv2.putText(output_img, plate_text, (x, y-10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(0, 255, 0),
                thickness=2,
                lineType=cv2.LINE_AA)

f, axes = plt.subplots(1, 3, figsize=(10, 5))
axes[0].imshow(canny)
axes[1].imshow(output_img)
if plate_img is not None:
    axes[2].imshow(plate_img)
plt.show()