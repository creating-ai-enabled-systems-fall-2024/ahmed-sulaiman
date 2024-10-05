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

def capture_udp_stream(stream_url):
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('UDP Stream', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

