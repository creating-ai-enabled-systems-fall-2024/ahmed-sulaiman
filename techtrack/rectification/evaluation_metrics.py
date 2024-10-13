import numpy as np

def compute_iou(box1, box2):
    x1_min = box1[0] - box1[2] / 2
    y1_min = box1[1] - box1[3] / 2
    x1_max = box1[0] + box1[2] / 2
    y1_max = box1[1] + box1[3] / 2

    x2_min = box2[0] - box2[2] / 2
    y2_min = box2[1] - box2[3] / 2
    x2_max = box2[0] + box2[2] / 2
    y2_max = box2[1] + box2[3] / 2

    x_inter_min = max(x1_min, x2_min)
    y_inter_min = max(y1_min, y2_min)
    x_inter_max = min(x1_max, x2_max)
    y_inter_max = min(y1_max, y2_max)

    inter_area = max(0, x_inter_max - x_inter_min) * max(0, y_inter_max - y_inter_min)

    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)

    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area != 0 else 0


def compute_precision_recall(predictions, ground_truths, iou_threshold=0.5):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    total_ground_truths = len(ground_truths)

    predictions = sorted(predictions, key=lambda x: x[1], reverse=True)

    matched_ground_truths = set()

    for pred in predictions:
        pred_class, confidence, x, y, w, h = pred
        pred_box = [x, y, w, h]

        match_found = False
        for i, gt in enumerate(ground_truths):
            gt_class, gt_x, gt_y, gt_w, gt_h = gt
            gt_box = [gt_x, gt_y, gt_w, gt_h]

            if pred_class == gt_class:
                iou = compute_iou(pred_box, gt_box)
                if iou >= iou_threshold and i not in matched_ground_truths:
                    match_found = True
                    true_positives += 1
                    matched_ground_truths.add(i)
                    break

        if not match_found:
            false_positives += 1

    false_negatives = total_ground_truths - true_positives

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0

    return precision, recall


def compute_average_precision(precisions, recalls):

    precisions = np.array(precisions)
    recalls = np.array(recalls)

    sorted_indices = np.argsort(recalls)
    recalls = recalls[sorted_indices]
    precisions = precisions[sorted_indices]

    ap = 0.0
    for i in range(len(precisions) - 1):
        ap += precisions[i] * (recalls[i+1] - recalls[i])

    return ap


def compute_mAP(predictions_dict, ground_truths_dict, iou_threshold=0.5, num_classes=80):
    ap_per_class = {}

    for class_id in range(num_classes):
        precisions = []
        recalls = []

        for image_id in predictions_dict.keys():
            predictions = predictions_dict[image_id]
            ground_truths = ground_truths_dict[image_id]

            predictions_for_class = [p for p in predictions if p[0] == class_id]
            ground_truths_for_class = [g for g in ground_truths if g[0] == class_id]

            precision, recall = compute_precision_recall(predictions_for_class, ground_truths_for_class, iou_threshold)
            precisions.append(precision)
            recalls.append(recall)

        ap_per_class[class_id] = compute_average_precision(precisions, recalls)

    mAP = np.mean(list(ap_per_class.values()))
    return mAP
