import numpy as np
from matplotlib import pyplot as plt

from augmentation import ColorTransformer, GeometricTransformer, NoiseTransformer, apply_pipeline
from utils import resize, load_all_jpg_images

images = []
all_imgs, _ = load_all_jpg_images('./archive')
for img in all_imgs:
    images.append(resize(img))

"""
Ожидаемый результат - numpy массив images с изображениями из датасета, 
приведенными к единому размеру: 100х100x3 с сохранением соотношения сторон.
"""

images_count = len(images)
print(f"images in RAM {images_count}")

"""
Применение аугментации. Ожидаемый результат - 5 аугментированных изображений.
"""
colorTransformer = ColorTransformer()
geometricTransformer = GeometricTransformer()
noiseTransformer = NoiseTransformer()

transformation_pipeline_1 = [colorTransformer, noiseTransformer, geometricTransformer]
transformation_pipeline_2 = [geometricTransformer, colorTransformer, noiseTransformer]
transformation_pipeline_3 = [noiseTransformer, geometricTransformer, colorTransformer]
transformation_pipeline_4 = [colorTransformer, geometricTransformer, noiseTransformer]

target_img = images[np.random.randint(0, images_count-1)]

f, axes = plt.subplots(1, 5, figsize=(15, 5))
axes[0].imshow(target_img[..., ::-1])
augmented_image = apply_pipeline(target_img, transformation_pipeline_1)
axes[1].imshow(augmented_image[..., ::-1])
augmented_image = apply_pipeline(target_img, transformation_pipeline_2)
axes[2].imshow(augmented_image[..., ::-1])
augmented_image = apply_pipeline(target_img, transformation_pipeline_3)
axes[3].imshow(augmented_image[..., ::-1])
augmented_image = apply_pipeline(target_img, transformation_pipeline_4)
axes[4].imshow(augmented_image[..., ::-1])
plt.show()