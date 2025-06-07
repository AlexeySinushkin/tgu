import cv2
from matplotlib import pyplot as plt
from augmentation import apply_augmentation
from ocr import get_text, prepare_plate_img, calculate_cer
from plate_extract_haar import preprocess


def apply_pipeline(path, plate_text):
    img = cv2.imread(path)
    img = apply_augmentation(img)
    output_img, plate_coord = preprocess(img.copy())
    plate_img = None
    if plate_coord is not None:
        x, y, w, h = plate_coord
        plate_img = output_img[y:y + h, x:x + w]
        plate_text_recognized = get_text(plate_img)
        print(f"original\t{plate_text}")
        print(f"detected\t{plate_text_recognized}")
        cer = calculate_cer(plate_text, plate_text_recognized)
        print(f"CER: {cer}")


    f, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(output_img)
    if plate_img is not None:
        axes[1].imshow(plate_img)
    plt.show()

apply_pipeline('car1.jpg', 'н764ке 799')
apply_pipeline('car2.jpg', 'с005км 190')
apply_pipeline('car3.jpg', 'а715ае 977')