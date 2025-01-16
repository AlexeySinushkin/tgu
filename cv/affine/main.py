import numpy as np
import matplotlib.pyplot as plt
# https://en.wikipedia.org/wiki/Affine_transformation


def warp_affine(image, M, output_shape):
    """
    Применяет афинное преобразование к изображению.

    Параметры:
        image: numpy.ndarray
            Входное изображение.
        M: numpy.ndarray
            Матрица афинного преобразования 3x3.
        output_shape: tuple
            Размер выходного изображения в формате (rows, cols, channels).

    Возвращает:
        numpy.ndarray
            Изображение после афинного преобразования.
    """
    height, width, _ = image.shape  # Определяем размеры исходного изображения
    out_height, out_width, _ = output_shape # Определяем размеры выходного изображения

    # Создаем пустой массив для результата
    output = np.zeros(output_shape, dtype=image.dtype)

    # Итерируемся по каждому пикселю выходного изображения
    for x in range(width):
        for y in range(height):
            # Преобразуем координаты пикселя из выходного пространства в входное
            transformed_x, transformed_y,  _ = np.dot(M, [x, y,  1]).astype(int)

            # Проверяем, находятся ли преобразованные координаты внутри границ входного изображения
            if 0 <= transformed_x < out_width and 0 <= transformed_y < out_height:
                # Копируем значение пикселя из входного изображения в выходное
                output[transformed_y, transformed_x, :] = image[y, x, :]

    return output

def get_image():
    return plt.imread("street_2.jpeg")

def rotate180():
    # загрузка картинки
    image = get_image()
    # угол поворота картинки
    th = np.radians(180)

# https://stackoverflow.com/questions/8275882/one-step-affine-transform-for-rotation-around-a-point
#A rotation of angle a around the point (x,y) corresponds to the affine transformation:
#CGAffineTransform transform = CGAffineTransformMake(cos(a),sin(a),-sin(a),cos(a),x-x*cos(a)+y*sin(a),y-x*sin(a)-y*cos(a));
    x = image.shape[1]/2
    y = image.shape[0]/2
    l = x-x*np.cos(th)+y*np.sin(th)
    m = y-x*np.sin(th)-y*np.cos(th)
    # задаем матрицу транфсормации
    M = np.float32(
        [[np.cos(th), np.sin(th), l],
        [-np.sin(th), np.cos(th), m],
        [0,0,0]],)

    # Размер выходного изображения
    shape=(image.shape[0], image.shape[1], image.shape[2])

    # применяем афинное преобразование
    result = warp_affine(image, M, shape)
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(image)
    plt.subplot(122)
    plt.title("Transformed")
    plt.imshow(result)
    #plt.tight_layout()
    plt.show()

def rotate90CCW():
    # загрузка картинки
    image = get_image()
    height, width, _ = image.shape
    # угол поворота картинки
    th = np.radians(90)
    # задаем матрицу транфсормации
    M = np.float32(
        [[np.cos(th), np.sin(th), 0],
        [-np.sin(th), np.cos(th), width],
        [0,0,1]],)

    # Размер выходного изображения
    shape=(width, height, image.shape[2])

    # применяем афинное преобразование
    result = warp_affine(image, M, shape)
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(image)
    plt.subplot(122)
    plt.title("Transformed")
    plt.imshow(result)
    #plt.tight_layout()
    plt.show()

rotate90CCW()