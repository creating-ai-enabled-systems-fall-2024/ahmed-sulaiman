import os
import numpy as np
import mistralai
from mistralai import Mistral
from modules.extraction.preprocessing import DocumentProcessing
from modules.extraction.embedding import Embedding
from modules.retrieval.indexing import FaissIndex 
from modules.retrieval.reranker import Reranker
from modules.retrieval.search import FaissSearch 

class Pipeline:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_type='brute_force', reranker_type='hybrid', mistral_api_key=None, generator_model='mistral-small-latest'):
        self.embedding = Embedding(model_name=model_name)
        self.document_processor = DocumentProcessing()
        self.index = FaissIndex(index_type=index_type)
        self.reranker = Reranker(type=reranker_type)
        self.search = FaissSearch(faiss_index=self.index)
        self.mistral_api_key = mistral_api_key
        self.generator_model = generator_model
        self.mistral_client = Mistral(api_key=self.mistral_api_key)
        
    def __encode(self, query):
        return self.embedding.encode([query])[0] 

    def search_neighbors(self, query_embedding, k=10):
        if self.index.index is None or self.index.index.ntotal == 0:
            raise ValueError("FAISS index is empty. Make sure to add embeddings to the index before searching.")
        
        print("Number of vectors in the FAISS index:", self.index.index.ntotal)

        if k is None:
            k = 10
        
        distances, _, neighbors = self.search.search(np.array([query_embedding]), k=k)
        return neighbors, distances
    
    def generate_answer(self, query, context, rerank=True):
        if rerank:
            context, _, _ = self.reranker.rerank(query, context)

        combined_context = " ".join(context)

        prompt = f"Answer the question: '{query}' based on the following context: {combined_context}"

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        response = self.mistral_client.chat.complete(
            model=self.generator_model,
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    def preprocess_corpus(self, corpus_directory, chunking_strategy, fixed_length=None, overlap_size=2):

        indexed_chunks = []
        
        for filename in os.listdir(corpus_directory):
            file_path = os.path.join(corpus_directory, filename)
            text = self.document_processor._DocumentProcessing__read_text_file(file_path)

            if chunking_strategy == 'sentence':
                chunks = self.document_processor.sentence_chunking(file_path, overlap_size)
            elif chunking_strategy == 'fixed-length' and fixed_length is not None:
                chunks = self.document_processor.fixed_length_chunking(text, fixed_length, overlap_size)
            else:
                raise ValueError("Invalid chunking strategy or parameters provided.")

            for chunk in chunks:
                embedding = self.embedding.encode([chunk])[0].reshape(1, -1)
                self.index.add_embeddings(embedding, metadata=[chunk])
                self.search = FaissSearch(faiss_index=self.index)
