import abc
import numpy as np
import cv2
import random
"""
Написание классов-оберток для функций преобразований, чтобы осущесвлять случайные преобразования.
Ожидаемый результат - корректно работающие обертки для любых 3 цветовых преобразований,
любых 5 геометических, 1 наложения шума или сглаживания на выбор.
"""

class ImageTransformer(abc.ABC):
    @abc.abstractmethod
    def random_transform(self, img: np.ndarray) -> np.ndarray:
        pass


class ColorTransformer(ImageTransformer):
    def random_transform(self, img: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Random hue (-10 to +10), saturation (0.8–1.2), brightness (0.8–1.2)
        hue_shift = random.uniform(-1, 1)
        sat_mult = random.uniform(0.9, 1.1)
        val_mult = random.uniform(0.9, 1.1)

        hsv[..., 0] = (hsv[..., 0] + hue_shift) % 180
        hsv[..., 1] *= sat_mult
        hsv[..., 2] *= val_mult

        # Clip and convert back
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

class GeometricTransformer(ImageTransformer):
    def random_transform(self, img: np.ndarray) -> np.ndarray:
        h, w = img.shape[:2]

        transform_type = random.choice([
           "crop", "zoom", "shift", "perspective"
        ])

        if transform_type == "crop":
            start_x = random.randint(0, w // 10)
            start_y = random.randint(0, h // 10)
            end_x = w - random.randint(0, w // 10)
            end_y = h - random.randint(0, h // 10)
            cropped = img[start_y:end_y, start_x:end_x]
            return cv2.resize(cropped, (w, h))

        elif transform_type == "zoom":
            scale = random.uniform(0.8, 1.2)
            resized = cv2.resize(img, None, fx=scale, fy=scale)
            if scale < 1:
                pad_w = (w - resized.shape[1]) // 2
                pad_h = (h - resized.shape[0]) // 2
                return cv2.copyMakeBorder(resized, pad_h, pad_h, pad_w, pad_w,
                                          borderType=cv2.BORDER_REFLECT)
            else:
                return resized[:h, :w]

        elif transform_type == "shift":
            dx = random.randint(-w // 2, w // 2)
            dy = random.randint(-h // 2, h // 2)
            matrix = np.float32([[1, 0, dx], [0, 1, dy]])
            return cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

        elif transform_type == "perspective":
            pts1 = np.float32([[0,0], [w,0], [0,h], [w,h]])
            offset = 0.02 * min(h, w)
            pts2 = pts1 + np.random.uniform(-offset, offset, pts1.shape).astype(np.float32)
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            return cv2.warpPerspective(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

        return img

class NoiseTransformer(ImageTransformer):
    def random_transform(self, img: np.ndarray) -> np.ndarray:
        noise_type = random.choice(["gaussian", "poisson", "salt", "pepper"])
        output = img.copy()

        if noise_type == "gaussian":
            mean = 0
            sigma = 10
            gauss = np.random.normal(mean, sigma, img.shape).astype(np.int16)
            output = np.clip(img.astype(np.int16) + gauss, 0, 255).astype(np.uint8)

        elif noise_type == "poisson":
            noisy = np.random.poisson(img.astype(np.float32))
            output = np.clip(noisy, 0, 255).astype(np.uint8)

        elif noise_type == "salt":
            amount = 0.01
            num_salt = int(amount * img.size)
            coords = [np.random.randint(0, i - 1, num_salt) for i in img.shape[:2]]
            output[coords[0], coords[1]] = 255

        elif noise_type == "pepper":
            amount = 0.01
            num_pepper = int(amount * img.size)
            coords = [np.random.randint(0, i - 1, num_pepper) for i in img.shape[:2]]
            output[coords[0], coords[1]] = 0

        return output


colorTransformer = ColorTransformer()
geometricTransformer = GeometricTransformer()
noiseTransformer = NoiseTransformer()
default_transformations = [colorTransformer, noiseTransformer, geometricTransformer]

def apply_augmentation(img: np.ndarray, transformations=default_transformations) -> np.ndarray:
    transformed_img = img.copy()
    for transform in transformations:
        transformed_img = transform.random_transform(transformed_img)
    return transformed_img