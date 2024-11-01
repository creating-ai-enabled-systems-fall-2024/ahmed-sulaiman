import os
from modules.extraction.preprocessing import DocumentProcessing
from modules.extraction.embedding import Embedding

class Pipeline:
    def __init__(self):
        self.document_processor = DocumentProcessing()
        self.embedding_model = Embedding('all-MiniLM-L6-v2')

    def preprocess_corpus(self, corpus_directory, chunking_strategy, fixed_length=None, overlap_size=2):

        indexed_chunks = []
        
        # Process each file in the corpus directory
        for filename in os.listdir(corpus_directory):
            file_path = os.path.join(corpus_directory, filename)
            text = self.document_processor._DocumentProcessing__read_text_file(file_path)

            # Apply chunking strategy
            if chunking_strategy == 'sentence':
                # Use the correct method name here
                chunks = self.document_processor.sentence_chunking(file_path, overlap_size)
            elif chunking_strategy == 'fixed-length' and fixed_length is not None:
                chunks = self.document_processor.fixed_length_chunking(text, fixed_length, overlap_size)
            else:
                raise ValueError("Invalid chunking strategy or parameters provided.")

            # Embed each chunk
            for chunk in chunks:
                embedding = self.embedding_model.encode(chunk)
                indexed_chunks.append({'chunk': chunk, 'embedding': embedding})
        
        return indexed_chunks

