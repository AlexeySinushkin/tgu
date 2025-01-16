import matplotlib.pyplot as plt
import cv2


def find_and_draw(path_to_train, path_to_test):
    # Считывание изображения
    image_1 = cv2.imread(path_to_train)
    # Конвертируем исходное изображение в RGB
    training_image = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
    # Конвертируем исходное изображение в gray scale
    training_gray = cv2.cvtColor(training_image, cv2.COLOR_RGB2GRAY)

    image_2 = cv2.imread(path_to_test)
    # Преобразование цветов из BGR в RGB
    image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
    test_image = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
    test_gray = cv2.cvtColor(test_image, cv2.COLOR_RGB2GRAY)

    # Создаем инстанс (экземпляр класса) SIFT метода
    #https://stackoverflow.com/questions/64525121/sift-surf-module-cv2-cv2-has-no-attribute-xfeatures2d-set-opencv-enabl
    sift = cv2.xfeatures2d.SIFT_create()

    # Найдем ключевые точки на исходном и тестовым снимках
    train_keypoints, train_descriptor = sift.detectAndCompute(training_gray, None)
    test_keypoints, test_descriptor = sift.detectAndCompute(test_gray, None)

    # Создаем объект прямого алгоритма сопоставления
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)

    # Сопостовляем признаковое описание (128-элементные векторы) между исходным и тестовым снимкам
    matches = bf.match(train_descriptor, test_descriptor)

    # Результаты с наименьшим расстоянием (между векторами) - то что нужно
    matches = sorted(matches, key=lambda x: x.distance)


    result = cv2.drawMatches(training_image, train_keypoints, test_gray, test_keypoints, matches[:100], test_gray, flags=2)
    # Отображаем лучшие ключевые точки
    plt.rcParams['figure.figsize'] = [14.0, 7.0]
    plt.title('Best Matching Points')
    plt.imshow(result)
    plt.show()

    print("\nNumber of Matching Keypoints Between The Training and Query Images: ", len(matches))

find_and_draw("street_1.jpeg", "street_2.jpeg")