import torch
from ESRGAN.models import RRDBNet  # Adjust based on ESRGAN repository structure

# Load ESRGAN model
class ESRGAN:
    def __init__(self, model_path='ESRGAN/models/RRDB_ESRGAN_x4.pth'):
        self.model = RRDBNet(3, 3, 64, 23, gc=32)
        self.model.load_state_dict(torch.load(model_path), strict=True)
        self.model.eval()
        if torch.cuda.is_available():
            self.model = self.model.cuda()
    
    def upscale(self, frame):
        # Convert frame to RGB and normalize
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_tensor = torch.from_numpy(frame_rgb).float().div(255).permute(2, 0, 1).unsqueeze(0)
        if torch.cuda.is_available():
            frame_tensor = frame_tensor.cuda()
        
        with torch.no_grad():
            upscaled_tensor = self.model(frame_tensor)
        
        upscaled_frame = upscaled_tensor.squeeze().cpu().clamp(0, 1).permute(1, 2, 0).numpy() * 255
        upscaled_frame = upscaled_frame.astype(np.uint8)
        return cv2.cvtColor(upscaled_frame, cv2.COLOR_RGB2BGR)

# Initialize ESRGAN
esrgan = ESRGAN()