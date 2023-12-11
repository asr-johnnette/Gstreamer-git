import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QMainWindow):
    def __init__(self, rtsp_url):
        super().__init__()

        self.setWindowTitle('GStreamer RTSP Player')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_widget = QVideoWidget(self.central_widget)
        self.video_widget.setGeometry(0, 0, 800, 480)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # Set up custom GStreamer pipeline
        self.media_player.setMedia(QMediaContent(QUrl.fromUserInput(rtsp_url)))

        # Play the RTSP stream automatically
        self.media_player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get camera IP address from user
    device_ip = input("Enter the IP address of the camera: ")

    # Create a GStreamer-compatible RTSP URL
    rtsp_url = f'rtspsrc location=rtsp://{device_ip}:1935/stream ! rtph264depay ! h264parse ! avdec_h264 ! identity drop-allocation=true ! autovideosink sync=false'

    # Start the PyQt video player with the same RTSP URL
    video_player = VideoPlayer(rtsp_url=rtsp_url)
    video_player.show()

    sys.exit(app.exec_())
