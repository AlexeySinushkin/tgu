import matplotlib.pyplot as plt
import numpy as np
import cv2

def show_images(images):
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(images[0])
    plt.subplot(122)
    plt.title("Corners Detected")
    plt.imshow(images[1])
    #plt.tight_layout()
    plt.show()

def Harris_corners(path):
    # Считывание изображения
    image = cv2.imread(path)

    # Преобразование цветов из BGR в RGB
    image_original = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Преобразование изображения в градации серого
    gray = cv2.cvtColor(image_original, cv2.COLOR_RGB2GRAY)
    gray = np.float32(gray)

    # Обнаружение углов
    dst = cv2.cornerHarris(gray, 2, 3, 0.05)

    # Нормализация результата для корректного отображения
    dst_normalized = cv2.normalize(dst, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    dst_normalized = np.uint8(dst_normalized)

    # Это значение зависит от изображения и количества углов, которые вы хотите обнаружить
    # Попробуйте изменить этот свободный параметр (0.1), сделав его больше или меньше, и посмотрите результат
    thresh = 110

    # Создание копии изображения для отображения углов
    corner_image = np.copy(image_original)

    # Проход по всем углам и их отрисовка на изображении (если они проходят пороговое значение)
    for j in range(0, dst.shape[0]):
        for i in range(0, dst.shape[1]):
            if dst_normalized[j, i] > thresh:
                # параметры: изображение, точка центра, радиус, цвет, толщина
                cv2.circle(corner_image, (i, j), 1, (0, 255, 0), 5)

    show_images((image_original, corner_image))

Harris_corners("street_2.jpeg")