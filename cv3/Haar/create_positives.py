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

# Папки
output_dir = "positives"
os.makedirs(output_dir, exist_ok=True)
os.makedirs("annotations", exist_ok=True)

# Параметры
augment_per_image = 10
output_txt_path = "positives.txt"

def augment_image(img, bbox):
    x, y, w, h = bbox
    objects = []

    for i in range(augment_per_image):
        img_aug = img.copy()
        rows, cols = img.shape[:2]

        # Смещения
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        ds = random.uniform(0.95, 1.05)

        # Новые координаты
        x_aug = int(max(0, x + dx))
        y_aug = int(max(0, y + dy))
        w_aug = int(min(cols - x_aug, w * ds))
        h_aug = int(min(rows - y_aug, h * ds))

        # Простейшие трансформации
        if random.random() < 0.3:
            img_aug = cv2.GaussianBlur(img_aug, (3, 3), 0)
        if random.random() < 0.3:
            img_aug = cv2.convertScaleAbs(img_aug, alpha=random.uniform(0.9, 1.1), beta=random.randint(-10, 10))

        # Имя
        filename = f"{os.path.splitext(os.path.basename(img_path))[0]}_aug{i}.jpg"
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, img_aug)
        objects.append((filename, x_aug, y_aug, w_aug, h_aug))

    return objects

# Основной цикл
all_entries = []

for img_path, bbox in annotations.items():
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Не удалось загрузить {img_path}")
        continue

    entries = augment_image(img, bbox)
    all_entries.extend(entries)

# Сохраняем positives.txt
with open(output_txt_path, "w") as f:
    for name, x, y, w, h in all_entries:
        f.write(f"{name} 1 {x} {y} {w} {h}\n")

print(f"✅ Сохранено {len(all_entries)} файлов в {output_dir}")
print(f"📄 Аннотация: {output_txt_path}")