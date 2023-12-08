import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class VideoPlayer(QMainWindow):
    def __init__(self, rtsp_url):
        super().__init__()

        self.setWindowTitle('GStreamer RTSP Player')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_widget = QLabel(self.central_widget)
        self.video_widget.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.video_widget)

        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)  # Update every 50 milliseconds

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_widget.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get camera IP address from user
    device_ip = input("Enter the IP address of the camera: ")

    rtsp_url = f'rtsp://{device_ip}:8554/fpv_stream'

    # Start the PyQt video player with the Herelink RTSP URL
    video_player = VideoPlayer(rtsp_url)
    video_player.show()

    sys.exit(app.exec_())
