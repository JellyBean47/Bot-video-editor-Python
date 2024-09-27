import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import torch
from PIL import Image
from torchvision import transforms
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from skimage import exposure

# ---------- U2NET Class ----------
class U2NET:
    def __init__(self, model_path='U-2-Net/saved_models/u2net/u2net_scripted.pth'):
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
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img = self.transform(image_pil).unsqueeze(0)
        if torch.cuda.is_available():
            img = img.cuda()
        
        # Predict mask
        with torch.no_grad():
            d1 = self.model(img)[0]
        # Post-process mask
        pred = d1.squeeze().cpu().numpy()
        pred = (pred - pred.min()) / (pred.max() - pred.min())
        mask = (pred * 255).astype(np.uint8)
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        return mask

# ---------- ESRGAN Class ----------
from ESRGAN.models import RRDBNet  # Adjust based on ESRGAN repository structure

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

# ---------- Enhancement Functions ----------
def enhance_lighting_contrast(frame):
    # Convert to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L-channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels back
    enhanced_lab = cv2.merge((l, a, b))
    
    # Convert back to BGR color space
    enhanced_frame = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # Further contrast adjustment using gamma correction
    enhanced_frame = exposure.adjust_gamma(enhanced_frame, gamma=1.2)  # Adjust gamma as needed
    
    return enhanced_frame

def enhance_background(frame, mask):
    # Convert mask to 3 channels
    mask_3ch = cv2.merge([mask, mask, mask])
    
    # Blur the background
    blurred_frame = cv2.GaussianBlur(frame, (21, 21), 0)
    
    # Combine blurred background with original foreground
    enhanced_frame = np.where(mask_3ch == 0, blurred_frame, frame)
    
    return enhanced_frame

# ---------- Initialize Models ----------
u2net = U2NET()
esrgan = ESRGAN()

# ---------- Frame Processing Function ----------
def process_frame(frame):
    # Step 1: Enhance lighting and contrast
    enhanced = enhance_lighting_contrast(frame)
    
    # Step 2: Enhance background
    mask = u2net.predict(enhanced)
    enhanced_bg = enhance_background(enhanced, mask)
    
    # Step 3: Upscale the frame
    upscaled = esrgan.upscale(enhanced_bg)
    
    return upscaled

# ---------- Video Processing Function ----------
def process_video(input_path, output_path):
    # Load video using MoviePy
    clip = VideoFileClip(input_path)
    
    # Set up the progress bar
    total_frames = int(clip.fps * clip.duration)
    progress_bar = tqdm(total=total_frames, desc="Processing Video", unit="frame")
    
    # Process frames
    def frame_processor(frame):
        processed = process_frame(frame)
        progress_bar.update(1)
        return processed
    
    # Apply enhancement to each frame
    edited_clip = clip.fl_image(frame_processor)
    
    # Save the edited video
    edited_clip.write_videofile(output_path, codec='libx264', fps=clip.fps)
    progress_bar.close()

# ---------- GUI Functions ----------
def select_input_video():
    file_path = filedialog.askopenfilename(title="Select Input Video", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_video():
    file_path = filedialog.asksaveasfilename(title="Select Output Video", defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def start_processing():
    input_path = input_entry.get()
    output_path = output_entry.get()
    
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select both input and output video files.")
        return
    
    # Run processing in a separate thread to keep the GUI responsive
    threading.Thread(target=run_processing, args=(input_path, output_path)).start()

def run_processing(input_path, output_path):
    try:
        process_video(input_path, output_path)
        messagebox.showinfo("Success", f"Video processed successfully!\nSaved at: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# ---------- Create the GUI ----------
def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("AI Video Editing Bot")
    
    # Create and place widgets
    tk.Label(root, text="Input Video:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_input_video).grid(row=0, column=2, padx=10, pady=10)
    
    tk.Label(root, text="Output Video:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_output_video).grid(row=1, column=2, padx=10, pady=10)
    
    tk.Button(root, text="Start Processing", command=start_processing, bg='green', fg='white').grid(row=2, column=1, pady=20)
    
    # Start the GUI loop
    root.mainloop()

# ---------- Main Execution ----------
if __name__ == "__main__":
    create_gui()
