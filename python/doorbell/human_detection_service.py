import threading
from threading import Thread

import cv2
from cv2 import VideoCapture
from matplotlib.dates import drange
from pyparsing import Empty

from dao.abstract_event_store import AbstractEventStore
from model.search_area import SearchArea


class EventProducerService(threading.Thread):
    def __init__(self, stream: VideoCapture, area: SearchArea, consumer: AbstractEventStore):
        threading.Thread.__init__(self)
        self.stream = stream
        self.area = area
        self.consumer = consumer
        # initialize the HOG descriptor
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def run(self):
        frame_index = 0
        while True:
            ret, frame = self.stream.read()
            print(f'frame index {frame_index}')
            frame_index += 1
            if not ret:
                break

            frame2 = cv2.resize(frame, (800, 600)) #FIXME
            if frame_index % 20 == 0:
                target_area = self.area.crop(frame2)
                # detect humans in input image
                (humans, _) = self.hog.detectMultiScale(target_area)
                # getting no. of human detected
                humans_count = len(humans)
                if humans_count is not Empty:
                    self.draw_rect_around_human(frame2, humans)
                    file_name = self.save_frame(frame2)
                    self.consumer.create(file_name)




    def draw_rect_around_human(self, frame, humans):
        # loop over all detected humans
        for (x, y, w, h) in humans:
            x, y, = self.area.translate_coordinates_to_original(frame, x, y)
            pad_w, pad_h = int(0.15 * w), int(0.01 * h)
            rect_x1 = x + pad_w
            rect_y1 = y + pad_h
            rect_x2 = x + w - pad_w
            rect_y2 = y + h - pad_h
            cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)

    def save_frame(self, frame) -> str:
        cv2.imwrite('./event-images/123.png', frame)
        return '123.png'