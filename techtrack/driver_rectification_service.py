from rectification.hard_negative_mining import compute_loss, sample_hard_negatives, evaluate_model_mAP, load_image_and_annotations
from rectification.augmentation import apply_augmentations
from modules.inference.object_detection import Model

if __name__ == "__main__":
    logistics_dir = 'datasets/logistics'
    
    model = Model(
        weights_path='datasets/yolo_model_2/yolov4-tiny-logistics_size_416_2.weights', 
        config_path='datasets/yolo_model_2/yolov4-tiny-logistics_size_416_2.cfg', 
        class_names_path='datasets/yolo_model_2/logistics.names'
    )    
    print("Loading images and annotations...")
    images_and_annotations = load_image_and_annotation(logistics_dir)
    
    losses = []
    for image, annotations in images_and_annotations:
        predictions = model.predict(image)
        processed_predictions = model.post_process(image, predictions, score_threshold=0.5)
        
        loss = compute_loss(processed_predictions[0], annotations)
        losses.append((image, loss))
    
    losses.sort(key=lambda x: x[1], reverse=True)
    top_n_hard_negatives = losses[:10] 
    
    print("Top-N hard negatives selected:")
    for idx, (image, loss) in enumerate(top_n_hard_negatives):
        print(f"Image {idx}: Loss = {loss}")
    
    print("Applying augmentations to hard negatives...")
    for image, loss in top_n_hard_negatives:
        augmented_images = apply_augmentations(image)
        
        for idx, aug_img in enumerate(augmented_images):
            output_path = f"output/augmented_image_{idx}.jpg"
            cv2.imwrite(output_path, aug_img)
            print(f"Augmented image saved: {output_path}")
    
    print("Evaluating mAP...")
    mAP = evaluate_model_mAP(predictions_dir, annotations_dir, model, iou_threshold=0.5)
    print(f"Mean Average Precision (mAP): {mAP}")
    
    print("Processing complete.")
