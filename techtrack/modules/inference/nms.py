import cv2
import numpy as np

def filter(bboxes, class_ids, scores, nms_iou_threshold):
    if len(bboxes) == 0 or len(scores) == 0:
        return [], [], []
    
    indices = cv2.dnn.NMSBoxes(bboxes, scores, score_threshold=0.5, nms_threshold=nms_iou_threshold)
    
    if indices is None or len(indices) == 0:
        return [], [], []
    
    if isinstance(indices, np.ndarray):
        indices = indices.flatten()

    filtered_bboxes = [bboxes[i] for i in indices]
    filtered_class_ids = [class_ids[i] for i in indices]
    filtered_scores = [scores[i] for i in indices]

    return filtered_bboxes, filtered_class_ids, filtered_scores
