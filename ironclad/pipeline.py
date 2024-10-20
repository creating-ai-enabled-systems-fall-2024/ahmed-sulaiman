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
    
    def encode(self, image):
        # Check if the input is already a PIL image
        if isinstance(image, torch.Tensor):
            preprocessed_image = image  # It's already a tensor
        elif isinstance(image, Image.Image):  # If it's a PIL image, preprocess it
            preprocessed_image = self.extractor.preprocess(image)
        else:
            # Otherwise, assume it's a file path and open the image
            preprocessed_image = self.extractor.preprocess(Image.open(image)) 

        # Extract embedding from the preprocessed image
        embedding = self.extractor.extract_embedding_tensor(preprocessed_image)
        return embedding
    
    def precompute(self, gallery_directory='datasets/multi_image_identities/multi_image_gallery'):
        embeddings = []
        self.gallery_filenames = []
        
        # Traverse each subdirectory (identity) in the gallery directory
        for root, dirs, files in os.walk(gallery_directory):
            for filename in files:
                if filename.endswith(('.jpg', '.png')):
                    image_path = os.path.join(root, filename)

                    # Encode the image into an embedding
                    embedding = self.encode(image_path)
                    if embedding is not None:
                        embeddings.append(embedding)
                        
                        # Store the filename associated with the embedding
                        identity = os.path.basename(root)
                        self.gallery_filenames.append((identity, filename))
        
        # Ensure embeddings are added to the FAISS index
        if embeddings:
            print(f"Number of embeddings to add: {len(embeddings)}")  # Debugging output
            self.indexer.add_embeddings(np.vstack(embeddings))
            print(f"Number of embeddings added to FAISS: {len(embeddings)}")
            print(f"Number of gallery filenames: {len(self.gallery_filenames)}")
        else:
            print("No embeddings were generated from the gallery.")
    
    def save_embeddings(self, filepath='storage/catalog/faiss_index.bin'):
        self.indexer.save_index(filepath)
    
    # def search_gallery(self, probe_directory='datasets/multi_image_identities/probe', k=5):
    #     results = {}

    #     # Traverse each subdirectory (identity) in the probe directory
    #     for root, dirs, files in os.walk(probe_directory):
    #         for filename in files:
    #             if filename.endswith(('.jpg', '.png')):
    #                 image_path = os.path.join(root, filename)
                    
    #                 # Load and encode the image
    #                 image = Image.open(image_path)
    #                 probe_embedding = self.encode(image)  # Encode the image to get the embedding

    #                 # Ensure the embedding is a 2D array
    #                 probe_embedding = np.array(probe_embedding).reshape(1, -1)

    #                 # Use the Searcher class to perform the FAISS search
    #                 searcher = Searcher(self.indexer, self.gallery_filenames)
    #                 neighbors = searcher.search_gallery(probe_embedding, k)

    #                 # Store the results for this probe image
    #                 identity = os.path.basename(root)
    #                 results[(identity, filename)] = neighbors

    #     return results

    def search_gallery(self, probe_embedding, k=5):
        # Ensure the embedding is in the correct format (2D array)
        if probe_embedding.ndim == 1:
            probe_embedding = probe_embedding.reshape(1, -1)
        
        # Perform the FAISS search using the Searcher class
        searcher = Searcher(self.indexer, self.gallery_filenames)
        neighbors = searcher.search_gallery(probe_embedding, k)

        return neighbors


    def load_index(self, filepath='storage/catalog/faiss_index.bin'):
        self.indexer.load_index(filepath)
