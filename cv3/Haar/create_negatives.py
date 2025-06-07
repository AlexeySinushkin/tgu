import cv2
import os
import random
import numpy as np

# Координаты: (x, y, w, h) для каждой картинки
annotations = {
    "../car1.jpg": (479, 412, 187, 33),
    "../car2.jpg": (661, 392, 192, 40),
    "../car3.jpg": (519, 374, 199, 40),
}

output_dir = "negatives"
os.makedirs(output_dir, exist_ok=True)

samples_per_image = 10
patch_size = (300, 300)
index = 0

def boxes_overlap(a, b):
    """ Проверка: пересекаются ли 2 прямоугольника a и b """
    ax1, ay1, aw, ah = a
    ax2, ay2 = ax1 + aw, ay1 + ah

    bx1, by1, bw, bh = b
    bx2, by2 = bx1 + bw, by1 + bh

    return not (bx2 <= ax1 or bx1 >= ax2 or by2 <= ay1 or by1 >= ay2)

for img_path, plate_box in annotations.items():
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Не удалось загрузить {img_path}")
        continue

    h_img, w_img = img.shape[:2]
    attempts = 0
    generated = 0

    while generated < samples_per_image and attempts < 100:
        attempts += 1

        # Случайная вырезка
        x = random.randint(0, w_img - patch_size[0])
        y = random.randint(0, h_img - patch_size[1])
        candidate_box = (x, y, patch_size[0], patch_size[1])

        if boxes_overlap(candidate_box, plate_box):
            continue  # Пропускаем, если пересекается с номером

        patch = img[y:y + patch_size[1], x:x + patch_size[0]]
        out_name = f"neg_{index}.jpg"
        cv2.imwrite(os.path.join(output_dir, out_name), patch)
        index += 1
        generated += 1

print(f"✅ Сохранено {index} негативных образцов в {output_dir}")