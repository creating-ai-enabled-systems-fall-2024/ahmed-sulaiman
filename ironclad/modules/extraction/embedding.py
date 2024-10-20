from facenet_pytorch import InceptionResnetV1
from PIL import Image
import torch
import numpy as np
from torchvision import transforms

class EmbeddingExtractor:
    def __init__(self, model='vggface2', device='cpu'):
        self.device = torch.device(device)
        self.model = InceptionResnetV1(pretrained=model).eval().to(self.device)
       
    def extract_embedding(self, image_path):
        # Load and preprocess image if it's a file path
        image = Image.open(image_path)
        preprocessed_image = self.__preprocess(image)
        return self.extract_embedding_tensor(preprocessed_image)

    def extract_embedding_tensor(self, preprocessed_image):
        # Generate embedding from preprocessed tensor
        with torch.no_grad():
            embedding = self.model(preprocessed_image.unsqueeze(0).to(self.device)).cpu().numpy()
        return embedding

    def preprocess(self, image):
        preprocess = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        return preprocess(image)

