from PIL import Image
import torchvision.transforms as transforms

class ImageProcessor:
    def __init__(self, image_size=(160, 160)):
        self.image_size = image_size
        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])  
        ])
    
    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        preprocessed_image = self.transform(image)
        return preprocessed_image
