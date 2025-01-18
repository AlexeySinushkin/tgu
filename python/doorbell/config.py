from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # it will be used test/test_video.mp4 as video stream
    test_mode:bool = False
    #setup environment variable before launch
    # Linux set RTSP_PASSWORD=mypassword
    # Windows set RTSP_PASSWORD mypassword
    rtsp_password: str
    rtsp_url: str = "rtsp://admin:{}@192.168.2.117:554/ISAPI/Streaming/Channels/101"

    def get_rtsp_url(self) -> str:
        return self.rtsp_url.format(self.rtsp_password)

settings = Settings()