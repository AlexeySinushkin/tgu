from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # it will be used test/test_video.mp4 as video stream
    test_mode:bool = True
    doorbell_sound_file: str = "resources/doorbell-26896.mp3"
    test_video_file: str = "resources/test_video.mp4"
    test_images_dir: str = "resources/event-images"
    #setup environment variable before launch
    # Linux set RTSP_PASSWORD=mypassword
    # Windows set RTSP_PASSWORD mypassword
    rtsp_password: str
    rtsp_url: str = "rtsp://admin:{}@192.168.2.117:554/ISAPI/Streaming/Channels/101"

    def get_rtsp_url(self) -> str:
        return self.rtsp_url.format(self.rtsp_password)

settings = Settings()