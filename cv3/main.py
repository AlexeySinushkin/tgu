import cv2
import numpy as np


def detect_plate_number(image_path):
    # Шаг 1: Загрузка изображения в черно-белом формате
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        raise FileNotFoundError(f"Изображение не найдено: {image_path}")

    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 100, 200)

    cv2.imshow("Detected Plates", canny)
    cv2.waitKey(0)

    # Шаг 4: Морфологические операции
    # Закрытие: помогает соединить вертикальные контуры букв
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel_close)

    # Эрозия: отделяет табличку от лишних элементов
    kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    eroded = cv2.erode(closed, kernel_erode, iterations=1)

    # Шаг 5: Поиск контуров
    contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Шаг 6: Фильтрация контуров по пропорциям
    plate_candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if 4.2 < aspect_ratio < 4.9 and w > 100 and h > 20:  # Можно скорректировать по размеру
            plate_candidates.append((x, y, w, h))

    # Шаг 7: Возвращаем найденные таблички или одну (например, первую)
    result_img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    for (x, y, w, h) in plate_candidates:
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return result_img, plate_candidates  # Вернём изображение и координаты табличек

output_img, plates = detect_plate_number("car3.jpg")
cv2.imshow("Detected Plates", output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()