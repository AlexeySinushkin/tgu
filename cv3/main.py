import cv2
import numpy as np
from matplotlib import pyplot as plt

def detect_plate_number(image_path):
    # Шаг 1: Загрузка изображения в черно-белом формате
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        raise FileNotFoundError(f"Изображение не найдено: {image_path}")

    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 100, 200)

    # Шаг 5: Поиск контуров
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)

    # Шаг 6: Фильтрация контуров по пропорциям
    plate_candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        #if 4.2 < aspect_ratio < 4.9 and w > 100 and h > 20:
        if 3.2 < aspect_ratio < 4.9 and w > 100 and h > 20:
            plate_candidates.append((x, y, w, h))

    # Шаг 7: Возвращаем найденные таблички или одну (например, первую)
    result_img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    for (x, y, w, h) in plate_candidates:
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return canny, result_img, plate_candidates  # Вернём изображение и координаты табличек

canny, output_img, plates = detect_plate_number("car2.jpg")

f, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(canny[...])
axes[1].imshow(output_img[...])
plt.show()