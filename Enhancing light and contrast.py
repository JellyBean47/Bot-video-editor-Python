import cv2
import numpy as np
from skimage import exposure

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