import cv2

image = cv2.imread('../car1.jpg')
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, -3, 1.0)
image = cv2.warpAffine(image, M, (w, h))
cv2.imwrite('pattern_source.jpg', image)
