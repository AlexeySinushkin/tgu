import numpy as np
import matplotlib.pyplot as plt



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
    rows, cols, *_ = image.shape  # Определяем размеры исходного изображения
    out_rows, out_cols, *_ = output_shape # Определяем размеры выходного изображения

    # Создаем пустой массив для результата
    output = np.zeros(output_shape, dtype=image.dtype)

    # Итерируемся по каждому пикселю выходного изображения
    for out_row in range(out_rows):
        for out_col in range(out_cols):
            # Преобразуем координаты пикселя из выходного пространства в входное
            in_col, in_row, _ = np.dot(M, [out_col, out_row, 1]).astype(int)

            # Проверяем, находятся ли преобразованные координаты внутри границ входного изображения
            if 0 <= in_row < rows and 0 <= in_col < cols:
                # Копируем значение пикселя из входного изображения в выходное
                output[out_row, out_col, :] = image[in_row, in_col, :]

    return output

def get_image():
    return plt.imread("street_2.jpeg")

def rotate():
    # загрузка картинки
    image = get_image()
    # угол поворота картинки
    th = np.radians(180)

# https://stackoverflow.com/questions/8275882/one-step-affine-transform-for-rotation-around-a-point
#A rotation of angle a around the point (x,y) corresponds to the affine transformation:
#CGAffineTransform transform = CGAffineTransformMake(cos(a),sin(a),-sin(a),cos(a),x-x*cos(a)+y*sin(a),y-x*sin(a)-y*cos(a));
    x = image.shape[1]/2
    y = image.shape[0]/2

    # задаем матрицу транфсормации
    M = np.float32(
        [[np.cos(th), np.sin(th), x-x*np.cos(th)+y*np.sin(th)],
        [-np.sin(th), np.cos(th), y-x*np.sin(th)-y*np.cos(th)],
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

rotate()