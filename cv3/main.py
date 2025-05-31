import numpy as np
import onnxruntime as ort
import pytesseract
import cv2
from augmentation import ColorTransformer, GeometricTransformer, NoiseTransformer, apply_pipeline

colorTransformer = ColorTransformer()
geometricTransformer = GeometricTransformer()
noiseTransformer = NoiseTransformer()
transformations = [colorTransformer, noiseTransformer, geometricTransformer]

#Зашумляем
def apply_augmentation(img: np.ndarray) -> np.ndarray:
    transformed_img = img.copy()
    for transform in transformations:
        transformed_img = transform.random_transform(transformed_img)
    return transformed_img


#Вырезаем область с номером
#def get_clean_plate(preprocessed_img: np.ndarray) -> np.ndarray:
#    return plate_img
#plate_img = get_clean_plate(preprocessed_img)

#cars = [cv2.imread('car1.jpg'), cv2.imread('car2.jpg'), cv2.imread('car3.jpg')]
#preprocessed_img = apply_augmentation(cars[0])

# Load ONNX model
session = ort.InferenceSession("DB_TD500_resnet18.onnx", providers=['CPUExecutionProvider'])

# Image normalization parameters
input_height = 736
input_width = 1280
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

def preprocess(img):
    h, w = img.shape[:2]
    resized = cv2.resize(img, (input_width, input_height))
    img_norm = resized.astype(np.float32) / 255.
    img_norm = (img_norm - mean) / std
    img_trans = img_norm.transpose(2, 0, 1)
    input_blob = np.expand_dims(img_trans, axis=0).astype(np.float32)
    return input_blob, (w / input_width, h / input_height)

def is_plate_shape(box, min_area=500, aspect_range=(4.2, 5.0)):
    # Use bounding box for aspect ratio
    x, y, w, h = cv2.boundingRect(box)
    if w == 0 or h == 0:
        return False
    area = w * h
    aspect_ratio = w / h
    return area > min_area and aspect_range[0] <= aspect_ratio <= aspect_range[1]

def postprocess(prob_map, scale, thresh=0.3):
    bin_map = (prob_map > thresh).astype(np.uint8) * 255
    contours, _ = cv2.findContours(bin_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for cnt in contours:
        if cv2.contourArea(cnt) < 100:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box *= scale
        box = box.astype(int)
        if is_plate_shape(box):
            boxes.append(box)
    return boxes

# Load image
image = cv2.imread("car1.jpg")
input_blob, scale = preprocess(image)

# Run inference
outputs = session.run(None, {"input": input_blob})
output = outputs[0]  # Should be shape (1, 1, H, W)
if output.ndim == 4:
    prob_map = output[0, 0, :, :]
else:
    raise ValueError(f"Unexpected model output shape: {output.shape}")

# Get filtered license plate-shaped boxes
boxes = postprocess(prob_map, scale)

# Crop & OCR
for i, box in enumerate(boxes):
    rect = cv2.boundingRect(box)
    x, y, w, h = rect
    plate_roi = image[y:y+h, x:x+w]

    # Improve OCR via preprocessing
    gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    text = pytesseract.image_to_string(thresh, config='--psm 7')
    print(f"[{i}] Plate Text: {text.strip()}")

    # Draw box and show
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.imshow(f"plate_{i}", plate_roi)

cv2.imshow("Detected Plates", image)
cv2.waitKey(0)
cv2.destroyAllWindows()