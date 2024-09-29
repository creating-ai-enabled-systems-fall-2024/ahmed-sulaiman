import cv2
import numpy as np

class Model:
    def __init__(self, weights_path, config_path, class_names_path):
        self.net = cv2.dnn.readNet(weights_path, config_path)
        with open(class_names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def predict(self, preprocessed_frame):
        blob = cv2.dnn.blobFromImage(preprocessed_frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_names = self.net.getUnconnectedOutLayersNames()
        outputs = self.net.forward(layer_names)
        return outputs

    def post_process(self, preprocessed_frame, predict_output, score_threshold):
        bboxes = []
        class_ids = []
        scores = []
        height, width = preprocessed_frame.shape[:2]
        for output in predict_output:
            for detection in output:
                scores_arr = detection[5:]
                class_id = np.argmax(scores_arr)
                confidence = scores_arr[class_id]
                if confidence > score_threshold:
                    bbox = detection[0:4] * np.array([width, height, width, height])
                    x, y, w, h = bbox.astype("int")
                    x = int(x - (w / 2))
                    y = int(y - (h / 2))
                    bboxes.append([x, y, int(w), int(h)])
                    class_ids.append(class_id)
                    scores.append(float(confidence))
        return bboxes, class_ids, scores