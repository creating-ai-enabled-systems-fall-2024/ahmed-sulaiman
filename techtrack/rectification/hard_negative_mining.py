import numpy as np
from evaluation_metrics import compute_iou, compute_mAP

def compute_loss(prediction, annotation):
    return np.mean((np.array(prediction) - np.array(annotation))**2)

def sample_hard_negatives(predictions_dir: str, annotations_dir: str, n: int) -> List[Tuple]:
    images_and_losses = []
    
    for filename in os.listdir(predictions_dir):
        pred_path = os.path.join(predictions_dir, filename)
        ann_path = os.path.join(annotations_dir, filename)
        
        prediction = load_predictions(pred_path)
        annotation = load_annotations(ann_path)
        
        loss = compute_loss(prediction, annotation)
        images_and_losses.append((filename, loss))
    
    images_and_losses.sort(key=lambda x: x[1], reverse=True)
    return images_and_losses[:n]

def image_entropy(image):
    hist = np.histogram(image, bins=256)[0]
    hist = hist / hist.sum()
    entropy = -np.sum(hist * np.log2(hist + 1e-7))  
    return entropy

def load_image_and_annotation(logistics_dir: str):
    images_and_annotations = []

    for filename in os.listdir(logistics_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(logistics_dir, filename)
            annotation_path = os.path.join(logistics_dir, filename.replace('.jpg', '.txt'))
            
            image = cv2.imread(image_path)

            if os.path.exists(annotation_path):
                with open(annotation_path, 'r') as f:
                    annotations = []
                    for line in f:
                        data = line.strip().split()
                        class_id = int(data[0])
                        x_center = float(data[1])
                        y_center = float(data[2])
                        width = float(data[3])
                        height = float(data[4])
                        annotations.append([class_id, x_center, y_center, width, height])
                
                images_and_annotations.append((image, annotations))

    return images_and_annotations

def load_image_and_annotation(logistics_dir: str):
    images_and_annotations = []

    for filename in os.listdir(logistics_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(logistics_dir, filename)
            annotation_path = os.path.join(logistics_dir, filename.replace('.jpg', '.txt'))
            
            image = cv2.imread(image_path)

            if os.path.exists(annotation_path):
                with open(annotation_path, 'r') as f:
                    annotations = []
                    for line in f:
                        data = line.strip().split()
                        class_id = int(data[0])
                        x_center = float(data[1])
                        y_center = float(data[2])
                        width = float(data[3])
                        height = float(data[4])
                        annotations.append([class_id, x_center, y_center, width, height])
                
                images_and_annotations.append((image, annotations))

    return images_and_annotations


def evaluate_model_mAP(predictions_dir: str, annotations_dir: str, iou_threshold: float = 0.5) -> float:
    predictions_dict = {}
    ground_truths_dict = {}

    for filename in os.listdir(predictions_dir):
        if filename.endswith('.jpg'):  # Only process image files
            pred_path = os.path.join(predictions_dir, filename.replace('.jpg', '.txt'))
            ann_path = os.path.join(annotations_dir, filename.replace('.jpg', '.txt'))

            predictions = load_predictions(pred_path)
            ground_truths = load_annotations(ann_path)

            image_id = filename.replace('.jpg', '')
            predictions_dict[image_id] = predictions
            ground_truths_dict[image_id] = ground_truths

    mAP = compute_mAP(predictions_dict, ground_truths_dict, iou_threshold=iou_threshold)
    return mAP