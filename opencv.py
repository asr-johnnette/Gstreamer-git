# import subprocess

# def open_gstreamer_pipeline(ip_address):
#     gstreamer_str = f"rtspsrc location=rtsp://{ip_address}:1935/stream ! rtph264depay ! h264parse ! avdec_h264 ! identity drop-allocation=true ! autovideosink sync=false"
    
#     try:
#         # subprocess.Popen(["gst-launch-1.0"] + gstreamer_str.split(), shell=False)
#         subprocess.Popen(["D:\\gstreamer\\1.0\\msvc_x86_64\\bin\\gst-launch-1.0"] + gstreamer_str.split(), shell=False)
#     except Exception as e:
#         print(f"Error opening GStreamer pipeline: {e}")

# if __name__ == "__main__":
#     camera_ip = input("Enter the IP address of the camera: ")
#     open_gstreamer_pipeline(camera_ip)


import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from imutils.video import VideoStream

class GStreamerPlayer(QWidget):
    def __init__(self, ip_address):
        super(GStreamerPlayer, self).__init__()

        self.ip_address = ip_address
        self.init_ui()

    def init_ui(self):
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label)

        self.gstreamer_pipeline = f"rtspsrc location=rtsp://{self.ip_address}:1935/stream ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"

        self.cap = cv2.VideoCapture(self.gstreamer_pipeline, cv2.CAP_GSTREAMER)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # Update every ~33 milliseconds (about 30 frames per second)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    camera_ip = input("Enter the IP address of the camera: ")

    player = GStreamerPlayer(camera_ip)
    player.setGeometry(100, 100, 800, 600)
    player.setWindowTitle("GStreamer Player")
    player.show()

    sys.exit(app.exec_())
