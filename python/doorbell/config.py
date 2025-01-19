from pydantic_settings import BaseSettings

from model.search_area import SearchArea


class Settings(BaseSettings):
    # it will be used test/test_video.mp4 as video stream
    test_mode:bool = True
    doorbell_sound_file: str = "resources/doorbell-26896.mp3"
    test_video_file: str = "resources/test_video.mp4"
    test_images_dir: str = "resources/event-images"
    #setup environment variable before launch
    # Linux set RTSP_PASSWORD=mypassword
    # Windows set RTSP_PASSWORD mypassword
    rtsp_password: str = ""
    #Для поиска по всему изображению нужны коэффициенты 0, 0, 1, 1
    #Это координаты левого верхнего угла (x, y) и правого нижнего (x, y)
    search_area: SearchArea = SearchArea(0.25, 0, 0.85, 0.5)
    rtsp_url: str = "rtsp://admin:{}@192.168.2.117:554/ISAPI/Streaming/Channels/101"

    def get_rtsp_url(self) -> str:
        return self.rtsp_url.format(self.rtsp_password)

settings = Settings()