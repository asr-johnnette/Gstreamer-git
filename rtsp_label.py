import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import subprocess

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

        # Set up RTSP stream
        self.media_player.setMedia(QMediaContent(QUrl(rtsp_url)))

        # Play the RTSP stream automatically
        self.media_player.play()

def connect_to_camera(ip_address):
    rtsp_url = f'rtsp://{ip_address}:8554/fpv_stream'
    print(f"RTSP URL: {rtsp_url}")
    
    # Run GStreamer pipeline in a subprocess
    subprocess.Popen(["gst-launch-1.0", f"rtspsrc location={rtsp_url} ! rtph264depay ! h264parse ! avdec_h264 ! identity drop-allocation=true ! autovideosink sync=false"], shell=True)

# import subprocess

# def connect_to_camera(ip_address):
#     # rtsp_url = f'rtsp://{ip_address}:8554/fpv_stream'
#     rtsp_url = f'rtsp://{ip_address}:1935/stream'
#     print(f"RTSP URL: {rtsp_url}")

#     # Run GStreamer pipeline in a subprocess using playbin
#     subprocess.Popen(["gst-launch-1.0", f'playbin uri={rtsp_url}'], shell=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get camera IP address from user
    device_ip = input("Enter the IP address of the camera: ")
    
    # Connect to the camera using GStreamer pipeline
    connect_to_camera(device_ip)

    # Start the PyQt video player with the same RTSP URL
    # video_player = VideoPlayer(rtsp_url=f'rtsp://{device_ip}:8554/fpv_stream')
    video_player = VideoPlayer(rtsp_url=f'rtsp://{device_ip}:1935/stream')
    video_player.show()

    sys.exit(app.exec_())
