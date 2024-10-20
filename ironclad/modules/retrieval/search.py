class Searcher:
    def __init__(self, indexer, gallery_filenames):
        self.indexer = indexer
        self.gallery_filenames = gallery_filenames
    
    def search_gallery(self, probe_embedding, k=5):
        distances, indices = self.indexer.search(probe_embedding, k)

        neighbors = []

        for idx in range(len(distances[0])):
            i = indices[0][idx]
            if i < len(self.gallery_filenames):
                neighbors.append((self.gallery_filenames[i], distances[0][idx]))
            else:
                print(f"Index {i} out of bounds for gallery filenames (length: {len(self.gallery_filenames)}).")

        return neighbors


