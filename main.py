import tkinter as tk
from tkinter import ttk
import ytd
import threading

def toggle_resolution_dropdown():
    if audio_only_var.get():
        resolution_dropdown.config(state=tk.DISABLED)
    else:
        resolution_dropdown.config(state=tk.NORMAL)

def download_video():
    # Disable the "Download" button to prevent multiple clicks
    download_button.config(state=tk.DISABLED)
    
    # Clear the status label
    status_label.config(text="")

    video_url = link_entry.get()
    resolution = resolution_var.get()
    audio_only = audio_only_var.get()
    options = {}
    options["video_url"] = video_url
    options["only_audio"] = audio_only
    options["resolution"] = resolution
    
    download_thread = threading.Thread(target=download_threaded, args=(options,))
    download_thread.start()

def download_threaded(options):
    status_label.config(text="Downloading..")
    try:
        ytd.download_video(options)
        status_label.config(text="Downloaded successfully")
    except Exception as e:
        status_label.config(text=f"Failed to download: {str(e)}")
    finally:
        download_button.config(state=tk.NORMAL)

window = tk.Tk()
window.title("YouTube Video Downloader")

link_label = ttk.Label(window, text="Enter YouTube Link:")
link_label.pack()
link_entry = ttk.Entry(window, width=40)
link_entry.pack()

resolution_label = ttk.Label(window, text="Select Resolution:")
resolution_label.pack()
resolutions = ['1080p', '720p', '480p', '360p', '240p', '144p']
resolution_var = tk.StringVar()
resolution_dropdown = ttk.Combobox(window, textvariable=resolution_var, values=resolutions)
resolution_dropdown.pack()

audio_only_var = tk.BooleanVar()
audio_only_checkbox = ttk.Checkbutton(window, text="Download Audio Only", variable=audio_only_var, command=toggle_resolution_dropdown)
audio_only_checkbox.pack()

download_button = ttk.Button(window, text="Download", command=download_video)
download_button.pack()

status_label = ttk.Label(window, text="")
status_label.pack()

toggle_resolution_dropdown()

window.mainloop()
