import cv2

# Путь к изображению
image_path = 'pattern_source.jpg'
output_annotation_file = 'positives.txt'
image_name = 'pattern_source.jpg'

# Создаём окно и читаем изображение
image = cv2.imread(image_path)
clone = image.copy()
roi = []

def select_roi(event, x, y, flags, param):
    global roi, image
    if event == cv2.EVENT_LBUTTONDOWN:
        roi = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        roi.append((x, y))
        cv2.rectangle(image, roi[0], roi[1], (0, 255, 0), 2)
        cv2.imshow("Select Number Plate", image)

# Запуск окна для выделения объекта
cv2.namedWindow("Select Number Plate")
cv2.setMouseCallback("Select Number Plate", select_roi)

print("Выдели номерной знак мышью (кликни и потяни), затем нажми любую клавишу...")
cv2.imshow("Select Number Plate", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Сохраняем аннотацию
if len(roi) == 2:
    x1, y1 = roi[0]
    x2, y2 = roi[1]
    x, y = min(x1, x2), min(y1, y2)
    w, h = abs(x2 - x1), abs(y2 - y1)
    with open(output_annotation_file, 'w') as f:
        f.write(f"{image_name} 1 {x} {y} {w} {h}\n")
    print(f"✅ Аннотация сохранена в {output_annotation_file}")
else:
    print("❌ Объект не был выделен.")