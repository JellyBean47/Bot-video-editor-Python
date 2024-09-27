#6. Creating a Simple GUI
#We'll use tkinter to create a simple GUI that allows users to select input and output videos and start the processing.

import tkinter as tk
from tkinter import filedialog, messagebox
import threading

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

#Explanation:

#GUI Components:
#Input Video Selection:
# Allows the user to select the input video file.

#Output Video Selection:
# Allows the user to specify the output video file path.

#Start Processing Button:
# Begins the video processing in a separate thread to keep the GUI responsive.

#Functionality:
#The GUI uses tkinter to create a window with labels, entry fields, and buttons.
#When the user clicks "Start Processing,"
# it validates the input, then calls the process_video function in a separate thread.
#Upon completion, it notifies the user with a success or error message.