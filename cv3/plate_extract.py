import cv2


def preprocess(image):
    # Загрузка изображения в черно-белом формате
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 100, 200)

    # Поиск контуров
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)
    contours = sorted(contours, key=cv2.contourArea)
    # Фильтрация контуров по пропорциям
    plate_candidate = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if 3.3 < aspect_ratio < 5.1 and w > 80 and h > 15:
            roi = canny[y:y + h, x:x + w]  # Вырезаем область из бинарного изображения
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

    # Возвращаем найденные таблички или одну (например, первую)
    result_img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    if plate_candidate is not None:
        x, y, w, h = plate_candidate
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return canny, result_img, plate_candidate