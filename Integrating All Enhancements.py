import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import torch
from PIL import Image
from torchvision import transforms

# Assuming the U2NET and ESRGAN classes are defined as above

# Initialize models
u2net = U2NET()
esrgan = ESRGAN()

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

def process_frame(frame):
    # Step 1: Enhance lighting and contrast
    enhanced = enhance_lighting_contrast(frame)
    
    # Step 2: Enhance background
    mask = u2net.predict(enhanced)
    enhanced_bg = enhance_background(enhanced, mask)
    
    # Step 3: Upscale the frame
    upscaled = esrgan.upscale(enhanced_bg)
    
    return upscaled

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

# Example usage
if __name__ == "__main__":
    input_video = "input_video.mp4"
    output_video = "enhanced_video.mp4"
    process_video(input_video, output_video)
    
    
 #   Explanation:

#Enhance Lighting and Contrast:
# Adjusts brightness and contrast using CLAHE and gamma correction.

#Enhance Background:
# Uses U2Net to create a mask separating the foreground and background. The background is blurred to make it look more professional.

#Upscale Frame:
# Uses ESRGAN to increase the resolution of the frame.

#Process Video:
# Reads the input video, processes each frame, and writes the enhanced video to the output path.