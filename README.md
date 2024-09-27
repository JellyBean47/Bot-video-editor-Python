# Bot-video-editor-python

(:This software is experimental and has not been tested as i do not have the neccacry resourses to test it:)

Prototype of a Python-based AI video editing bot that enhances video quality by
improving lighting, contrast, background, and resolution.
A touch of GUI added

The goal is to build an AI-powered video editing bot that:

Inputs: Takes a video file.
---------------------------
Processes:
Enhances lighting and contrast.
Enhances the background to make it look more professional.
Upscales the resolution for better quality.
----------------------------------------------------------
Outputs: Outputs the edited video.
----------------------------------------------------------
*Also add a user friendly GUI*

Prerequisites
Ensure you have the following:

Operating System: Windows
Python: Version 3.8 or above.
Hardware: A CUDA-compatible GPU is highly recommended for faster processing, especially for models like ESRGAN.
Internet Connection: To download necessary libraries and pre-trained models.
____________________________________________________________________________________________________________________________
1. Setting Up your Environment
Download Python
Visit the official Python website and download Python 3.8 or later.
Install Python
Run the installer.
Important: Check the box that says "Add Python to PATH" before clicking "Install Now."
____________________________________________________________________________________________________________________________
1.1 Install Required Python Libraries
Open Command Prompt and run the following commands to install the necessary libraries:

pip install opencv-python moviepy torch torchvision numpy scikit-image tqdm tkinter
Note:
torch and torchvision are essential for running deep learning models.
tkinter is included with Python, but if you encounter issues, you might need to install it separately.
____________________________________________________________________________________________________________________________
1.2 Install FFmpeg
FFmpeg is crucial for video processing.

Download FFmpeg:
Go to the FFmpeg Download Page.
Download the latest static build for Windows.
Install FFmpeg:

Extract the downloaded ZIP file to a folder, e.g., C:\ffmpeg.
Add FFmpeg to PATH:

Open System Properties > Advanced > Environment Variables.
Under System variables, find and select the Path variable, then click Edit.
Click New and add the path to FFmpeg's bin directory, e.g., C:\ffmpeg\bin.
Click OK to save changes.
Verify Installation:

Open Command Prompt and type ffmpeg -version. You should see FFmpeg version details.
____________________________________________________________________________________________________________________________
1.3 Downloading Pre-trained Models
a. ESRGAN (Enhanced Super-Resolution GAN)
Download ESRGAN Repository:

Visit the ESRGAN GitHub Repository.
Click on Code > Download ZIP or clone the repository using Git:
git clone https://github.com/xinntao/ESRGAN.git
Download Pre-trained Weights:
Navigate to the Pre-trained Models section.
Download the RRDB_ESRGAN_x4.pth model.
Place the Model:
Place the downloaded .pth file in the ESRGAN/models directory.

U2Net (Background Enhancement)
Download U2Net Repository:
Visit the U2Net GitHub Repository.
Click on Code > Download ZIP or clone the repository using Git:
bash
Copy code
git clone https://github.com/xuebinqin/U-2-Net.git
Download Pre-trained Weights:
Download the u2net.pth model from the Pre-trained Models section.
Place the Model:
Place the downloaded .pth file in the U-2-Net/saved_models/u2net directory.
____________________________________________________________________________________________________________________________
