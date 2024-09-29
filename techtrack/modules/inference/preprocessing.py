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