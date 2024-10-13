
# System_Report.md

## Running the System with Docker

To run the system, follow these steps:

1. **Install Docker**:
   Ensure that Docker is installed on your machine. You can download it from the official Docker website.
   
2. **Build the Docker Image**:
   You can build the Docker image using the provided `Dockerfile`:
   ```bash
   docker build -t techtrack_inference_service .
   ```

3. **Run the Docker Container**:
   To run the container, ensuring network accessibility for the UDP stream:
   ```bash
   docker run --network host techtrack_inference_service
   ```

4. **Dependencies**:
   - Python 3.8+
   - OpenCV (4.10.0)
   - NumPy
   - FFmpeg (for video streaming)
   - matplotlib/seaborn (for graphing and visualizations)
   - YOLOv4 model (weights and configuration)

---

## System Design

### Inference Service
The **Inference Service** is responsible for processing video streams, performing object detection, and saving the output with bounding boxes. It accepts a UDP stream, decodes the frames using OpenCV, and runs inference through the YOLOv4 model. It then processes the bounding boxes and saves the images with drawn boxes for visualization.

### Rectification Service
The **Rectification Service** is used to augment data and perform hard negative mining. It processes the logistics folder, selecting the hardest examples based on IoU loss and augmenting them to enhance model performance. This service also computes evaluation metrics such as mAP to measure model performance across the dataset.

---

## Metrics Definition

### Offline Metrics
**Offline metrics** are those used during model training and evaluation, providing insights into how well the system generalizes to unseen data. Examples include:
- **IoU (Intersection over Union)**: Measures how well the predicted bounding box overlaps with the ground truth. It's crucial for understanding the accuracy of object localization.
- **mAP (mean Average Precision)**: Used to evaluate the overall detection performance across different classes. This metric helps assess the precision and recall trade-offs.

### Online Metrics
**Online metrics** are used to monitor the system's performance in real-time or in a production setting. They include:
- **Latency**: Measures how fast the system processes each video frame. Ensuring low latency is essential for real-time applications.
- **Throughput**: Monitors how many frames the system can process in a given time period. This ensures that the system is scalable for different environments.

These online metrics would be monitored via logging systems like Prometheus and Grafana, or other monitoring tools to ensure that the system meets performance expectations in real-time deployments.

---

## Analysis of System Parameters and Configurations

### 1. **Choosing YOLO Model 2 Over YOLO Model 1**
One key design decision was selecting **YOLO Model 2** over **YOLO Model 1**. As seen in the graph depicting the **distribution of confidence scores** in the model_performance python notebook, Model 2 has a higher number of high-confidence predictions (centered around 0.8 to 0.9), while Model 1's confidence scores are more spread out. This suggests that Model 2 has more accurate detections, as it is more confident in its predictions.

Furthermore, the **bounding box widths and heights** from the same notebook show that Model 2 generates slightly smaller boxes on average than Model 1. This could indicate that Model 2 is more precise in predicting object sizes, which aligns with higher confidence scores. The combination of these factors led to selecting Model 2 as the preferred model for object detection.

| Model Comparison | Confidence Score | Bounding Box Widths | Bounding Box Heights |
|------------------|------------------|---------------------|----------------------|
| **Model 1**      | More spread out  | Slightly larger     | Larger, varied       |
| **Model 2**      | Higher confidence| Smaller, precise    | More consistent      |

### 2. **Drawing and Saving Bounding Boxes in the Inference Service**
A second design decision in the **Inference Service** was how to draw and save the bounding boxes. After running inference, we use OpenCV to overlay bounding boxes on the image frames and save them as `.jpg` images. This approach enables easy visualization of detections and helps in debugging and validating model output. The method also supports saving predictions in YOLO format for further use in evaluation or training. This decision simplifies tracking detection results during inference without sacrificing performance.

### 3. **Setting Up the Docker Container for the Inference Service**
Another critical design decision was how to set up the Docker container. We used the `--network host` option to allow the container to access the UDP stream from the host machine. This decision ensured that the video stream could be processed without any networking issues. Using Docker also makes the system more portable and easy to deploy, which is important for real-world use cases where the system may need to run on different servers or environments.

### 4. **Processing Images from the Logistics Folder in the Rectification Service**
For the **Rectification Service**, one design decision was how to efficiently process images and their annotations from the logistics folder. We structured the folder so that each image has a corresponding `.txt` file containing the YOLO annotations. This setup simplifies loading data for augmentation and hard negative mining, as each image can be paired with its ground truth annotations, facilitating loss calculations and subsequent augmentations.

### 5. **Using Both IoU and mAP for Evaluation**
A final significant decision was using both **IoU** and **mAP** for evaluation in the Rectification Service. The **IoU** metric was chosen for its precision in evaluating individual bounding boxes, while **mAP** offers a more comprehensive view of the model’s performance across all predictions and classes. This combination ensures that the system is optimized not only for localization (IoU) but also for overall detection accuracy (mAP). The decision to compute both metrics provided a more robust way to track model improvements, especially after hard negative mining and augmentations.

| Metric | Purpose |
|--------|---------|
| **IoU** | Measure localization accuracy on individual boxes. |
| **mAP** | Evaluate detection accuracy across all classes. |

---

### Conclusion

In summary, key design decisions such as selecting YOLO Model 2, handling bounding box predictions, setting up the Docker container, processing images efficiently, and using comprehensive evaluation metrics (IoU and mAP) all contributed to optimizing the system's performance. Each decision was made based on both quantitative (graphs and metrics) and qualitative analysis, ensuring that the system is scalable, portable, and accurate.