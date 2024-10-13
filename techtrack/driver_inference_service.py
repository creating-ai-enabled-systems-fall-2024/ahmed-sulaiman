import os
from modules.inference.object_detection import Model
from modules.inference.preprocessing import capture_udp_stream, capture_video
from modules.inference.inference_service import run_inference_service, draw_and_save_bounding_boxes, save_annotations

if __name__ == "__main__":
    stream_url = os.getenv('STREAM_URL', 'udp://127.0.0.1:23000')  
    drop_rate = int(os.getenv('DROP_RATE', '1')) 
    annotation_format = os.getenv('ANNOTATION_FORMAT', 'YOLO')

    model = Model(
        weights_path='datasets/yolo_model_2/yolov4-tiny-logistics_size_416_2.weights', 
        config_path='datasets/yolo_model_2/yolov4-tiny-logistics_size_416_2.cfg', 
        class_names_path='datasets/yolo_model_2/logistics.names'
    )

    run_inference_service(stream_url, drop_rate=drop_rate, annotation_format=annotation_format)