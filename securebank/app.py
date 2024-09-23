from flask import Flask, request, jsonify, render_template_string
from pipeline import Pipeline
from modules.feature_extractor import Feature_Extractor 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


app = Flask(__name__)

pipeline = Pipeline(version="LogisticRegression")

prediction_history = []

feature_extractor = Feature_Extractor()

@app.route('/')
def index():
    return render_template_string('''
        <h2>Welcome to the Fraud Detection API</h2>
        <form action="/form" method="get">
            <button type="submit">Go to Prediction Form</button>
        </form>
        <form action="/generate-dataset" method="post">
            <button type="submit">Generate New Training Dataset</button>
        </form>
        <form action="/audit" method="get">
            <button type="submit">Audit System Performance</button>
        </form>
    ''')

@app.route('/generate-dataset', methods=['POST'])
def generate_dataset():
    try:
        training_data, testing_data = feature_extractor.extract(
            'storage/dataset/train_data.parquet', 'storage/dataset/test_data.parquet'
        )

        training_data = training_data.sample(frac=0.1)
        testing_data = testing_data.sample(frac=0.1)
        
        feature_extractor.transform(training_data, testing_data)

        return render_template_string('''
            <h2>Dataset Generation</h2>
            <p>New training and testing datasets have been generated and saved successfully.</p>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        ''')
    except Exception as e:
        return jsonify({'error': f'Error generating dataset: {e}'}), 500

@app.route('/form')
def form():
    return render_template_string('''
        <h2>Fraud Detection Prediction Form</h2>
        <form action="/predict" method="post">
            <label for="model">Select Model:</label><br>
            <select name="model">
                <option value="LogisticRegression">Logistic Regression</option>
                <option value="NaiveBayes">Naive Bayes</option>
                <option value="ExtraTrees">Extra Trees</option>
            </select><br><br>
            
            <label for="trans_date_trans_time">Transaction Date/Time:</label><br>
            <input type="text" name="trans_date_trans_time" value="2024-09-22 12:30:00"><br><br>
            
            <label for="cc_num">Credit Card Number:</label><br>
            <input type="text" name="cc_num" value="1234567890123456"><br><br>

            <label for="unix_time">Unix Time:</label><br>
            <input type="text" name="unix_time" value="1632300000"><br><br>

            <label for="merchant">Merchant:</label><br>
            <input type="text" name="merchant" value="test_merchant"><br><br>

            <label for="category">Category:</label><br>
            <input type="text" name="category" value="test_category"><br><br>

            <label for="amt">Amount:</label><br>
            <input type="text" name="amt" value="150.00"><br><br>

            <label for="merch_lat">Merchant Latitude:</label><br>
            <input type="text" name="merch_lat" value="37.7749"><br><br>

            <label for="merch_long">Merchant Longitude:</label><br>
            <input type="text" name="merch_long" value="-122.4194"><br><br>

            <input type="submit" value="Submit">
            
        </form>
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    ''')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not request.is_json:
            data = {
                'trans_date_trans_time': request.form.get('trans_date_trans_time'),
                'cc_num': request.form.get('cc_num'),
                'unix_time': int(request.form.get('unix_time')),
                'merchant': request.form.get('merchant'),
                'category': request.form.get('category'),
                'amt': float(request.form.get('amt')),
                'merch_lat': float(request.form.get('merch_lat')), 
                'merch_long': float(request.form.get('merch_long')),
            }
            selected_model = request.form.get('model')
        else:
            data = request.get_json()
            selected_model = data.get('model')
        
        pipeline.select_model(selected_model)

        result = pipeline.predict(data)
        prediction_history.append((data, result))

        return render_template_string(f'''
            <h2>Prediction Result</h2>
            <p>The transaction is {'fraudulent' if result else 'legitimate'}</p>
            <form action="/form" method="get">
                <button type="submit">Make Another Prediction</button>
            </form>
        ''')

    except ValueError as e:
        return render_template_string(f'''
            <h2>Error</h2>
            <p>Invalid input: {e}</p>
            <form action="/form" method="get">
                <button type="submit">Go Back to Form</button>
            </form>
        '''), 400

@app.route('/audit', methods=['GET'])
def audit_performance():
    if not prediction_history:
        return render_template_string('''
            <h2>System Audit</h2>
            <p>No predictions have been made yet.</p>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        ''')

    y_true = []
    y_pred = []
    for record in prediction_history:
        data, prediction = record
        y_true.append(data.get('is_fraud')) 
        y_pred.append(prediction) 
    
    print(f"y_true: {y_true}")
    print(f"y_pred: {y_pred}")

    valid_values = {0, 1}
    if not all(value in valid_values for value in y_true) or not all(value in valid_values for value in y_pred):
        return jsonify({'error': 'y_true or y_pred contains invalid values'}), 400

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return render_template_string(f'''
        <h2>System Audit</h2>
        <h3>Performance Metrics</h3>
        <ul>
            <li>Accuracy: {accuracy:.2f}</li>
            <li>Precision: {precision:.2f}</li>
            <li>Recall: {recall:.2f}</li>
            <li>F1 Score: {f1:.2f}</li>
        </ul>
        <h3>Prediction History</h3>
        <p>{len(prediction_history)} predictions have been made.</p>
        <form action="/" method="get">
            <button type="submit">Back to Home</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
