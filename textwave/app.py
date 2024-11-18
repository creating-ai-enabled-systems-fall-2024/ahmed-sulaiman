from flask import Flask, request, jsonify
from textwave.pipeline import Pipeline

app = Flask(__name__)

pipeline = Pipeline(mistral_api_key='your_api_key_here')

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.json
    query = data.get("query")
    k = data.get("k", 10)
    rerank = data.get("rerank", True)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    query_embedding = pipeline._Pipeline__encode(query)
    neighbors, _ = pipeline.search_neighbors(query_embedding, k=k)

    answer = pipeline.generate_answer(query, neighbors, rerank=rerank)
    return jsonify({"query": query, "answer": answer})

@app.route('/add_documents', methods=['POST'])
def add_documents():
    data = request.json
    corpus_directory = data.get("corpus_directory")
    chunking_strategy = data.get("chunking_strategy", "sentence")
    fixed_length = data.get("fixed_length", None)
    overlap_size = data.get("overlap_size", 2)

    if not corpus_directory:
        return jsonify({"error": "Corpus directory is required"}), 400

    pipeline.preprocess_corpus(corpus_directory, chunking_strategy, fixed_length, overlap_size)
    return jsonify({"message": "Documents added successfully to the index"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
