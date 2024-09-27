import torch
from PIL import Image
from torchvision import transforms
import os

# Load U2Net model
class U2NET:
    def __init__(self, model_path='U-2-Net/saved_models/u2net/u2net.pth'):
        self.model = torch.jit.load(model_path).eval()
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        self.transform = transforms.Compose([
            transforms.Resize((320, 320)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406),
                                 (0.229, 0.224, 0.225))
        ])
    
    def predict(self, image):
        # Preprocess image
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img = self.transform(image).unsqueeze(0)
        if torch.cuda.is_available():
            img = img.cuda()
        
        # Predict mask
        with torch.no_grad():
            d1 = self.model(img)[0]
        # Post-process mask
        pred = d1.squeeze().cpu().numpy()
        pred = (pred - pred.min()) / (pred.max() - pred.min())
        mask = (pred * 255).astype(np.uint8)
        mask = cv2.resize(mask, (image.width, image.height))
        return mask

# Initialize U2Net
u2net = U2NET()