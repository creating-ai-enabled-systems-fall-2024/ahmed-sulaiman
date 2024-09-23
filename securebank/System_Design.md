
# SecureBank Fraud Detection System

## Instructions to Run the Application

### Prerequisites:
- Docker
- Python 3.9 or later
- Install required Python libraries (if running locally): 
  - `pip install -r requirements.txt`

### Running the Application (Docker):
1. Build the Docker image:
    ```
    docker build -t fraud-detection-app .
    ```
2. Run the container:
    ```
    docker run -p 5000:5000 fraud-detection-app
    ```
3. Access the application at `http://localhost:5000`.

---

## System Design

### How the System Design Meets the Requirements

- **R1: Improved Model Performance**  
  By enabling the retraining of models with new datasets and allowing administrators to select from a catalog of models, the system promotes continuous model improvement. Administrators can use the audit functionality to monitor performance and adjust configurations as needed.

- **R2: Transaction Prediction**  
  The system provides a simple API that can be accessed via a web form or programmatically. Users can submit transaction data, and the system will return whether the transaction is legitimate or fraudulent using the selected model.

- **R3: Dataset Generation**  
  Administrators can generate new datasets using the `/generate-dataset` endpoint. The system extracts and transforms data from existing sources (customers, transactions, fraud information), applies feature engineering, and prepares the dataset for training.

- **R4: Model Selection**  
  Administrators can choose from pre-trained models (e.g., Logistic Regression, Naive Bayes, Extra Trees) via the web form. The system dynamically loads the selected model and uses it for prediction.

- **R5: Performance Auditing**  
  The `/audit` endpoint allows administrators to track and evaluate the model's performance over time. This feature calculates metrics such as accuracy, precision, recall, and F1-score based on historical prediction data.

### System Components and Processes

1. **Data Extraction and Transformation**  
   - The `Raw_Data_Handler` and `Feature_Extractor` modules handle the extraction of raw data from `CSV`, `Parquet`, and `JSON` files, followed by transformation (e.g., scaling and encoding) to prepare the data for model training.

2. **Model Training and Selection**  
   - Models are trained in the `model_performance.ipynb` notebook using the transformed data. The system allows the selection of models from a catalog of pre-trained models, including Logistic Regression, Naive Bayes, and Extra Trees.

3. **Prediction and Inference**  
   - The `Pipeline` class handles the prediction process. It loads the pre-trained model, processes incoming transaction data, and outputs whether the transaction is likely to be fraudulent.

4. **Dataset Generation**  
   - Administrators can generate new datasets by re-extracting, transforming, and saving data using the `/generate-dataset` endpoint.

5. **Auditing and Monitoring**  
   - The `/audit` endpoint provides performance metrics, allowing administrators to assess the system’s effectiveness over time.

---

## Data, Data Pipelines, and Model

### Data Description
The data consists of customer, transaction, and fraud information:

- **Customer Data**: Contains customer demographic information.
- **Transaction Data**: Includes details of transactions (e.g., amount, merchant, location).
- **Fraud Data**: Binary labels indicating whether a transaction was fraudulent.

### Data Pipelines
- **Extract**: Data is extracted from CSV, Parquet, and JSON formats using `Raw_Data_Handler`.
- **Transform**: Data is transformed by `Feature_Extractor`, which applies scaling and encoding to prepare the dataset for model training.
- **Load**: The final cleaned and transformed dataset is stored in Parquet format for efficient access.

### Model Inputs and Outputs

- **Inputs**: The model expects features such as transaction amount, category, merchant, and location data (latitude/longitude).
- **Outputs**: The model returns a binary classification indicating whether a transaction is fraudulent.

---

## Metrics Definition

### Offline Metrics
- **Accuracy**: Measures the proportion of correctly predicted transactions.
- **Precision**: Assesses the accuracy of fraud predictions.
- **Recall**: Measures the model’s ability to identify all fraudulent transactions.
- **F1-score**: Balances precision and recall to give an overall performance score.

### Online Metrics
- **Prediction Latency**: Measures the time it takes for the system to return a fraud prediction.
- **Prediction Accuracy**: Monitors the accuracy of predictions made in real-time.

---

## Analysis of System Parameters and Configurations

### Feature Selection

Feature selection is crucial to identifying which data attributes (features) are most predictive in detecting fraudulent transactions. Key features used include:

- **amt** (Transaction Amount): Abnormal transaction amounts often indicate fraud.
- **category** (Transaction Category): Categories help reveal spending patterns.
- **merchant** (Merchant Name): Different merchants may show varying risks for fraud.
- **merch_lat** and **merch_long** (Merchant Latitude/Longitude): Geospatial data helps detect transactions in unusual locations.

**Preprocessing Pipeline:**
- **Numeric Features**: StandardScaler is applied to standardize `amt`, `merch_lat`, and `merch_long`.
- **Categorical Features**: OneHotEncoder is used for `category` and `merchant`.

By transforming these features, the system improves its ability to identify patterns indicative of fraud.

### Dataset Design

Designing the dataset to prevent data leakage is critical for a fraud detection system:

1. **Data Splitting**:
   - To avoid leakage, transactions of individual customers are kept entirely in either the training or testing set. This ensures the model is evaluated on unseen customers.
  
2. **Class Imbalance**:
   - Fraudulent transactions are rare. Techniques like **undersampling** or **oversampling** are applied to mitigate class imbalance and ensure the model does not overfit to the majority (legitimate) class.
  
3. **Cross-Validation**:
   - **k-fold cross-validation** is used to ensure the model generalizes well. This helps prevent overfitting and provides a more reliable performance estimate.

### Model Evaluation and Selection

We evaluated three models: **Logistic Regression**, **Naive Bayes**, and **Extra Trees Classifier**.

1. **Logistic Regression**:
   - A simple, interpretable model that serves as a baseline.
   - Works well for linear relationships between features and fraud outcomes but struggles with complex patterns.

2. **Naive Bayes**:
   - Suitable for categorical data and performs well with fraud detection features.
   - It tends to have higher recall (detecting more fraud cases) but lower precision, meaning more false positives.

3. **Extra Trees Classifier**:
   - The best-performing model, capable of handling complex relationships and large datasets.
   - Achieved the highest F1-score, balancing precision and recall effectively.

**Model Selection Process**:
- **Cross-validation** was used to evaluate models.
- **Metrics used**:
  - **Accuracy**: Percentage of correct predictions.
  - **Precision**: Accuracy of fraud predictions.
  - **Recall**: Ability to detect all fraudulent cases.
  - **F1-Score**: A balance between precision and recall.

The **Extra Trees Classifier** was chosen as the primary model based on its superior performance. However, administrators can switch between models as needed.

---

## Post-deployment Policies

### Monitoring and Maintenance Plan
- Regular auditing via the `/audit` endpoint helps track the system's performance. Alerts can be set up to notify administrators if performance metrics drop below a certain threshold.

### Fault Mitigation Strategies
- The system includes robust error handling, logging, and resource management to ensure smooth operation. Administrators can re-train models or generate new datasets if performance degrades over time.

