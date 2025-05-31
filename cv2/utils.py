import cv2
import numpy as np
import os

def load_all_jpg_images(root_dir):
    images = []
    paths = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                full_path = os.path.join(dirpath, filename)
                img = cv2.imread(full_path)

                if img is not None:
                    images.append(img)
                    paths.append(rel_path)
                else:
                    print(f"Warning: Failed to load {rel_path}")

    return images, paths

def resize(img, size=(100, 100)):
    old_h, old_w = img.shape[:2]
    new_h, new_w = size

    # Выбор интерполяции
    if old_h > new_h or old_w > new_w:
        interp = cv2.INTER_AREA  # лучше для уменьшения
    else:
        interp = cv2.INTER_CUBIC  # лучше для увеличения

    # Создаем холст из нулей (чёрный фон)
    new_img = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)

    ar = old_h / old_w
    if ar > 1:  # вертикальное изображение
        factor = new_h / old_h
        resize_h = new_h
        resize_w = int(old_w * factor)
    else:  # горизонтальное изображение или квадрат
        factor = new_w / old_w
        resize_w = new_w
        resize_h = int(old_h * factor)

    resized_img = cv2.resize(img, (resize_w, resize_h), interpolation=interp)

    # Вставляем центрированное изображение на холст
    start_ymin = max((new_h - resize_h) // 2, 0)
    start_xmin = max((new_w - resize_w) // 2, 0)

    new_img[start_ymin:start_ymin + resize_h, start_xmin:start_xmin + resize_w] = resized_img

    return new_img

