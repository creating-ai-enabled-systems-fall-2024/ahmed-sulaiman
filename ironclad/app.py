from flask import Flask, request, jsonify
from modules.extraction.embedding import EmbeddingExtractor
from modules.retrieval.index import Indexer
from pipeline import Pipeline

app = Flask(__name__)

pipeline = Pipeline(model='vggface2', device='cpu')
history = [] 

@app.route('/identify', methods=['POST'])
def identify():
    file = request.files['file']
    k = int(request.form.get('k', 5))
    
    image = pipeline.preprocess_image(file)
    embedding = pipeline.encode(image)
    
    neighbors = pipeline.search_gallery(embedding, k=k)
    
    history.append({'probe': file.filename, 'neighbors': neighbors})
    
    return jsonify(neighbors)

@app.route('/add', methods=['POST'])
def add_identity():
    file = request.files['file']
    identity = request.form['identity']
    
    image = pipeline.preprocess_image(file)
    pipeline.add_to_gallery(image, identity)
    
    return jsonify({"status": "success", "message": f"Added {identity} to the gallery"})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
