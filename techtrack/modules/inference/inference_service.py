import os
import sys
sys.path.append(os.path.abspath('../'))

import cv2
import json
from typing import List, Tuple
from modules.inference.object_detection import Model
from modules.inference.preprocessing import capture_udp_stream

os.makedirs('output/images', exist_ok=True)
os.makedirs('output/annotations', exist_ok=True)

def draw_and_save_bounding_boxes(frame, predictions: Tuple[List, List, List], frame_index: int):
    bboxes, class_ids, scores = predictions
    
    for bbox, class_id, score in zip(bboxes, class_ids, scores):
        x_min, y_min, x_max, y_max = bbox
        
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        label = f"{model.classes[class_id]}: {score:.2f}"
        cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    output_image_path = f'output/images/frame_{frame_index}.jpg'
    cv2.imwrite(output_image_path, frame)

def save_annotations(bboxes, class_ids, scores, frame_index, img_shape, format='YOLO'):
    annotation_path = f'output/annotations/frame_{frame_index}.txt' if format == 'YOLO' else f'output/annotations/frame_{frame_index}.json'
    height, width = img_shape[:2]
    
    if format == 'YOLO':
        with open(annotation_path, 'w') as f:
            for bbox, class_id, score in zip(bboxes, class_ids, scores):
                x_center = (bbox[0] + bbox[2]) / (2 * width)
                y_center = (bbox[1] + bbox[3]) / (2 * height)
                box_width = (bbox[2] - bbox[0]) / width
                box_height = (bbox[3] - bbox[1]) / height
                f.write(f"{class_id} {x_center} {y_center} {box_width} {box_height} {score}\n")
    
    elif format == 'PASCAL':
        annotation = {
            "image_id": frame_index,
            "annotations": [
                {
                    "class_id": class_id,
                    "bbox": [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]],
                    "score": score
                }
                for bbox, class_id, score in zip(bboxes, class_ids, scores)
            ]
        }
        with open(annotation_path, 'w') as f:
            json.dump(annotation, f, indent=4)

def run_inference_service(stream_url, drop_rate=1, annotation_format='YOLO'):

    print(f"Starting to capture video from {stream_url}...")
    
    if stream_url.startswith('udp://'):
        frame_generator = capture_udp_stream(stream_url, drop_rate)
    else:
        frame_generator = capture_video(stream_url, drop_rate)

    frame_index = 0

    for frame in frame_generator:
        predictions = model.post_process(frame, model.predict(frame), score_threshold=0.5)
        
        draw_and_save_bounding_boxes(frame, predictions, frame_index)
        
        save_annotations(*predictions, frame_index, frame.shape, format=annotation_format)
        
        frame_index += 1

    print(f"Inference complete. Images and annotations saved in the 'output/' directory.")
