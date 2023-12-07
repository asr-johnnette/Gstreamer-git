# import sys
# from PyQt5.QtWidgets import QApplication, QWidget

# app = QApplication(sys.argv)

# window = QWidget()
# window.setWindowTitle('Hello PyQt5')
# window.show()

# sys.exit(app.exec_())
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GStreamer RTSP Player')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_widget = QVideoWidget(self.central_widget)
        self.video_widget.setGeometry(0, 0, 800, 480)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # Set up RTSP stream
        rtsp_url = 'rtsp://192.168.1.17:1935\stream'
        self.media_player.setMedia(QMediaContent(QUrl(rtsp_url)))

        # Play the RTSP stream automatically
        self.media_player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
