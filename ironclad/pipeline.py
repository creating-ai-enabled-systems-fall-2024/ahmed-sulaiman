import os
import numpy as np
import torch
from modules.extraction.embedding import EmbeddingExtractor
from modules.retrieval.index import Indexer
from modules.retrieval.search import Searcher
from PIL import Image

class Pipeline:
    def __init__(self, model='vggface2', device='cpu'):
        self.extractor = EmbeddingExtractor(model=model, device=device)
        self.indexer = Indexer()
        self.gallery_filenames = []

    def preprocess_image(self, file):
        image = Image.open(io.BytesIO(file.read()))
        return self.extractor.preprocess(image)
    
    def encode(self, image):
        if isinstance(image, torch.Tensor):
            preprocessed_image = image  
        elif isinstance(image, Image.Image):
            preprocessed_image = self.extractor.preprocess(image)
        else:
            preprocessed_image = self.extractor.preprocess(Image.open(image)) 

        embedding = self.extractor.extract_embedding_tensor(preprocessed_image)
        return embedding
    
    def precompute(self, gallery_directory='datasets/multi_image_identities/multi_image_gallery'):
        embeddings = []
        self.gallery_filenames = []
        
        for root, dirs, files in os.walk(gallery_directory):
            for filename in files:
                if filename.endswith(('.jpg', '.png')):
                    image_path = os.path.join(root, filename)

                    embedding = self.encode(image_path)
                    if embedding is not None:
                        embeddings.append(embedding)
                        
                        identity = os.path.basename(root)
                        self.gallery_filenames.append((identity, filename))
        
        if embeddings:
            print(f"Number of embeddings to add: {len(embeddings)}")
            self.indexer.add_embeddings(np.vstack(embeddings))
            print(f"Number of embeddings added to FAISS: {len(embeddings)}")
            print(f"Number of gallery filenames: {len(self.gallery_filenames)}")
        else:
            print("No embeddings were generated from the gallery.")
    
    def save_embeddings(self, filepath='storage/catalog/faiss_index.bin'):
        self.indexer.save_index(filepath)
    

    def search_gallery(self, probe_embedding, k=5):
        if probe_embedding.ndim == 1:
            probe_embedding = probe_embedding.reshape(1, -1)
        
        searcher = Searcher(self.indexer, self.gallery_filenames)
        neighbors = searcher.search_gallery(probe_embedding, k)

        return neighbors
    
    def add_to_gallery(self, image, identity):
        embedding = self.encode(image)
        if embedding is not None:
            self.indexer.add_embeddings([embedding])  
            self.gallery_filenames.append(identity)   
            print(f"Added {identity} to the gallery.")
        else:
            print("Failed to generate embedding for the new identity.")


    def load_index(self, filepath='storage/catalog/faiss_index.bin'):
        self.indexer.load_index(filepath)
