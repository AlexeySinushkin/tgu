import cv2
from model.search_area import SearchArea

test_video_search_area = SearchArea(0.25, 0, 0.85, 0.5)
test_video_stream = cv2.VideoCapture("../resources/test_video.mp4")

# initialize the HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

frame_index = 0
while True:
  ret, frame = test_video_stream.read()
  print(f'frame index {frame_index}')
  frame_index+=1
  if not ret:
    break

  frame2 = cv2.resize(frame, (800, 600))
  humans_count = 0
  if frame_index % 20 == 0:
    target_area = test_video_search_area.crop(frame2)
    target_area_gray = cv2.cvtColor(target_area, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Search_area", target_area_gray)
    # detect humans in input image
    (humans, _) = hog.detectMultiScale(target_area)

    # getting no. of human detected
    humans_count = len(humans)
    print('Human Detected : ', humans_count)

    # loop over all detected humans
    for (x, y, w, h) in humans:
      x, y, = test_video_search_area.translate_coordinates_to_original(frame2, x, y)
      pad_w, pad_h = int(0.15 * w), int(0.01 * h)
      rect_x1 = x + pad_w
      rect_y1 = y + pad_h
      rect_x2 = x + w - pad_w
      rect_y2 = y + h - pad_h
      cv2.rectangle(frame2, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)

  # display the output image
  cv2.imshow("Image", frame2)
  if humans_count>0:
    cv2.waitKey(0)
    break
  key = cv2.waitKey(1)
  #Esc
  if key==27:
    cv2.destroyAllWindows()
    break
test_video_stream.release()
