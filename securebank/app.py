from flask import Flask, request, jsonify
from pipeline import Pipeline

app = Flask(__name__)

pipeline = Pipeline(version="LogisticRegression")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    required_fields = ['trans_date_trans_time', 'cc_num', 'unix_time', 'merchant', 'category', 'amt', 'merch_lat', 'merch_long']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    result = pipeline.predict(data)
    return jsonify({'fraudulent': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)