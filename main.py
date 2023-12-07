import subprocess

def connect_to_camera(ip_address):
    # gst-launch-1.0 rtspsrc location=rtsp://192.168.1.39:8554/fpv_stream ! rtph264depay ! h264parse ! avdec_h264 ! identity drop-allocation=true ! autovideosink sync=false
    pipeline_command = f"rtspsrc location=rtsp://{ip_address}:8554/fpv_stream ! rtph264depay ! h264parse ! avdec_h264 ! identity drop-allocation=true ! autovideosink sync=false"
    print(pipeline_command)

    # Run GStreamer pipeline in a subprocess
    subprocess.Popen(["gst-launch-1.0"] + pipeline_command.split(), shell=True)

if __name__ == "__main__":
    camera_ip = input("Enter the IP address of the camera: ")
    connect_to_camera(camera_ip)
