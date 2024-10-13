import cv2

def capture_video(filename, drop_rate):
    cap = cv2.VideoCapture(filename)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % drop_rate == 0:
            yield frame
        frame_count += 1
    cap.release()

def capture_udp_stream(stream_url, drop_rate = 1):
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
    frame_count = 0
    if not cap.isOpened():
        print(f"Error: Unable to open UDP stream at {stream_url}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % drop_rate == 0:
            yield frame
        frame_count += 1

    cap.release()

