import tkinter as tk
from tkinter import *
from tkinter import filedialog
import ffmpeg
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os


def down_video(url, save_path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)

        # Get the 1080p video-only stream and audio-only stream
        video_stream = yt.streams.filter(res="1080p", mime_type="video/mp4", only_video=True).first()
        audio_stream = yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()

        if not video_stream or not audio_stream:
            print("Required 1080p video or audio stream not available.")
            return

        # Download video-only and audio-only files
        video_file = video_stream.download(output_path=save_path, filename="temp_video.mp4")
        audio_file = audio_stream.download(output_path=save_path, filename="temp_audio.mp4")

        video_stream = ffmpeg.input(video_file)
        print(video_file)
        audio_stream = ffmpeg.input(audio_file)
        print(audio_file)

        output_file = os.path.join(save_path, yt.title + "_1080p.mp4")


        # Merge audio and video, copying the video codec and setting audio codec to AAC
        ffmpeg.output(video_stream, audio_stream, output_file, vcodec="copy", acodec="aac").run(overwrite_output=True)
        print(f"Successfully created {save_path}")


        # Clean up temporary files
        os.remove(video_file)
        os.remove(audio_file)

        print("Download and merge completed! Saved as:", output_file)

    except Exception as e:
        print("An error occurred:", e)


def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
    return folder

submitted_links = []

def submit():
    global submitted_links
    # Retrieve multi-line input and split by line to get each link
    submitted_links = text_box.get("1.0", END).strip().splitlines()
    if submitted_links:

        for link in submitted_links:
            print(link)
        # Close the window after submission
        window.destroy()
    else:
        print("Please enter one or more links.")

def clear():
    # Clear the Text widget
    text_box.delete("1.0", END)

# Set up the main window
window = Tk()
window.title("YouTube Downloader")
window.geometry("600x400")

# Instructions label
label = Label(window, text="Add YouTube Link Here To Download:", font=("Arial", 14))
label.pack(pady=10)

# Multi-line Text widget for entering links
text_box = Text(window, font=("Arial", 14), bg="#111111", fg="#00FF00", height=10, width=50)
text_box.pack(pady=10)

# Submit button
submit_button = Button(window, text="Download", command=submit)
submit_button.pack(side=LEFT, padx=20)

# Clear button
clear_button = Button(window, text="Clear", command=clear)
clear_button.pack(side=RIGHT, padx=20)

# Run the Tkinter main loop
window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window



    video_url = submitted_links


    save_dir = open_file_dialog()

    for link in video_url:
        if not save_dir:
            print("No valid save location selected.")
        else:
            down_video(link, save_dir)