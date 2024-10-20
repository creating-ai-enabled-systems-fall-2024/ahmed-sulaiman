import faiss
import os
import numpy as np

class Indexer:
    def __init__(self, dimension=512):
        self.index = faiss.IndexFlatL2(dimension)
    
    def add_embeddings(self, embeddings):
        self.index.add(embeddings)
    
    def save_index(self, filepath='storage/catalog/faiss_index.bin'):
        faiss.write_index(self.index, filepath)
    
    def load_index(self, filepath='storage/catalog/faiss_index.bin'):
        self.index = faiss.read_index(filepath)
    
    def search(self, probe_embedding, k=5):
        D, I = self.index.search(probe_embedding, k)  # FAISS expects a 2D array
        return D, I
