import threading
import time
from datetime import datetime

import cv2
from cv2 import VideoCapture
from pyparsing import Empty
from config import settings
from dao.abstract_event_store import AbstractEventStore
from dao.test_image_dao import save_image
from model.bell_event import BellEvent
from model.search_area import SearchArea
import pygame.mixer as sound

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
        last_saved_event: BellEvent | None = None
        sound.init()
        sound.music.load(settings.doorbell_sound_file)

        try:
            while True:
                ret, frame = self.stream.read()
                frame_index += 1
                if not ret:
                    time.sleep(1)
                    continue

                frame2 = cv2.resize(frame, (800, 600)) #FIXME
                if frame_index % 10 == 0:
                    target_area = self.area.crop(frame2)
                    # detect humans in input image
                    (humans, _) = self.hog.detectMultiScale(target_area)
                    # getting no. of human detected
                    humans_count = len(humans)
                    if humans_count is not Empty:
                        if last_saved_event is None:
                            self.draw_rect_around_human(frame2, humans)
                            file_name = self.save_frame(frame2)
                            last_saved_event = self.consumer.create(file_name)
                            print(f'new event {file_name}')
                            # TODO SRP move
                            sound.music.play()
                        else:
                            #Расширяем правую границу события (как долго человек находился в зоне интереса)
                            #TODO добавить еще изображений к этому событию
                            last_saved_event.stop_date = datetime.now()
                            self.consumer.update(last_saved_event)
                    elif last_saved_event is not None:
                        delta = datetime.now() - last_saved_event.stop_date
                        if delta.seconds>20:
                            last_saved_event = None
        finally:
            self.stream.release()




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
        new_file_name = save_image(frame)
        return new_file_name