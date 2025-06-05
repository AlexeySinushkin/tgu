import cv2
import numpy as np


def rotate(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def preprocess(image):
    # Загрузка изображения в черно-белом формате
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(img_gray, (5, 5), 1)
    canny = cv2.Canny(blurred, 70, 200)
    #kernel = np.ones((3, 3), np.uint8)  # Можно попробовать (5, 5) если разрывы больше
    #canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

    #крутим изображение, пока не найдет нужный контр с правильными пропорциями и площадью
    rotate_angles = [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6]

    plate_candidate = None
    rotated_canny = None
    found_angle = 0
    for angle in rotate_angles:
        rotated_canny = rotate(canny.copy(), angle)
        # Поиск контуров
        contours, _ = cv2.findContours(rotated_canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)
        contours = sorted(contours, key=cv2.contourArea)
        # Фильтрация контуров по пропорциям
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = w / float(h)
            if 140 < w < 250:
                print(f"{aspect_ratio} {w} {h} {angle}")
                cv2.rectangle(rotated_canny, (x, y), (x + w, y + h), (0, 100, 0), 1)
            if 4.1 < aspect_ratio < 5.0 and 140 < w < 250:
                roi = rotated_canny[y:y + h, x:x + w]  # Вырезаем область из бинарного изображения
                # Находим контуры внутри ROI
                inner_contours, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                letter_count = 0
                for lc in inner_contours:
                    _, _, lc_w, lc_h = cv2.boundingRect(lc)
                    if lc_w>10 and lc_h>25:
                        letter_count+=1
                if letter_count > 5:
                    plate_candidate = (x, y, w, h)
                    break
        if plate_candidate is not None:
            found_angle = angle
            break

    # Возвращаем найденные таблички или одну (например, первую)
    result_img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    if plate_candidate is not None:
        x, y, w, h = plate_candidate
        result_img = rotate(result_img, found_angle)
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return rotated_canny, result_img, plate_candidate