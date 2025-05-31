import cv2

from matplotlib import pyplot as plt
from pytesseract import pytesseract

from augmentation import apply_augmentation
from plate_extract import preprocess

img = cv2.imread("car3.jpg")
img = apply_augmentation(img)
canny, output_img, plate_coord = preprocess(img.copy())
plate_img = None
if plate_coord is not None:
    x, y, w, h = plate_coord
    plate_img = img[y:y + h, x:x + w]
    #EAST_model = cv2.dnn.TextDetectionModel_EAST('frozen_east_text_detection.pb')
    #EAST_model.setInputParams (1., (512, 512), (127.5, 127.5, 127.5), True)
    #boxes, confidences = EAST_model.detect (plate_img)
    text = pytesseract.image_to_string(plate_img, lang='eng', config='--psm 7')


f, axes = plt.subplots(1, 3, figsize=(10, 5))
axes[0].imshow(canny[...])
axes[1].imshow(output_img[...])
if plate_img is not None:
    axes[2].imshow(plate_img)
plt.show()