import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import hashlib
import os
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Success and failure messages
HASHY_SUCCESS = [
    "✨ Nailed it! Checksum is a match!",
    "🎉 You got it! 100% match.",
    "🤖 Hashy approves this file!"
]

happy_message_to_link = {
    "🤖 Hashy approves this file!" : "approves.mp3",
    "✨ Nailed it! Checksum is a match!" : "nailed it.mp3",
    "🎉 You got it! 100% match." : "you got it.mp3"
}


happy_music = [
    "nailed it.mp3",
    "you got it.mp3",
    "approves.mp3",
]

HASHY_FAIL = [
    "⚠️ Oops, that's not quite right...",
    "❌ No match! Hashy's circuits are confused.",
    "💔 Broken hash dreams. Try again?"
]

# Calculate checksum of file
def calculate_checksum(file_path, algorithm):
    try:
        hash_func = getattr(hashlib, algorithm)()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception:
        return None

# File browser dialog
def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filepath)

# Update hashy image based on emotion
def update_hashy_emotion(emotion):
    emotions = {
        "happy": "happy.png",
        "sad": "sad.png",
        "neutral": "noemo.png"
        
    }
    image = Image.open(emotions[emotion])
    image = image.resize((128, 128), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    hashy_label.config(image=photo)
    hashy_label.image = photo

# Play sound using pygame
def play_sound(file_name):
    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
    except Exception as e:
        print("⚠️ Sound error:", e)


sad_music = [
    "compressed/broken.mp3",
    "compressed/no match.mp3",
    "compressed/oops.mp3",
]

# Check checksum logic
def check_checksum():
    file_path = file_entry.get()
    given_checksum = checksum_entry.get().strip().lower()
    algorithm = algo_var.get()

    if not os.path.isfile(file_path):
        status_label.config(text="📁 File not found!", fg="red")
        update_hashy_emotion("sad")
        return

    if not given_checksum:
        status_label.config(text="🔍 Enter a checksum!", fg="orange")
        update_hashy_emotion("neutral")
        return

    result = calculate_checksum(file_path, algorithm)

    if result is None:
        status_label.config(text="💥 Error during hashing.", fg="red")
        update_hashy_emotion("sad")
    elif result == given_checksum:
        _text = random.choice(HASHY_SUCCESS)
        status_label.config(text=_text, fg="green")
        music = happy_message_to_link[_text]
        play_sound(music)
        update_hashy_emotion("happy")
    else:
        fail_message = random.choice(HASHY_FAIL)
        status_label.config(text=fail_message, fg="red")
        update_hashy_emotion("sad")
        # play_sound("compressed/no match.mp3")

        # Play corresponding sound
        if "Oops" in fail_message:
            play_sound("compressed/oops.mp3")
        elif "No match" in fail_message:
            play_sound("compressed/no match.mp3")
        elif "Broken" in fail_message:
            play_sound("compressed/broken.mp3")

# UI setup
root = tk.Tk()
root.title("Hashy – Checksum Checker with Emotion & Sound")
root.geometry("520x360")
root.configure(bg="#f0f8ff")
root.resizable(False, False)

# Hashy image
hashy_label = tk.Label(root, bg="#f0f8ff")
hashy_label.pack(pady=10)
update_hashy_emotion("neutral")

# File selection
file_frame = tk.Frame(root, bg="#f0f8ff")
file_frame.pack(fill='x', padx=10)
file_entry = tk.Entry(file_frame, width=50)
file_entry.pack(side='left', fill='x', expand=True)
tk.Button(file_frame, text="Browse", command=browse_file).pack(side='right')

# Checksum entry
tk.Label(root, text="Enter Checksum:", bg="#f0f8ff").pack(anchor='w', padx=10, pady=(10, 0))
checksum_entry = tk.Entry(root, width=60)
checksum_entry.pack(padx=10, fill='x')

# Algorithm dropdown
tk.Label(root, text="Select Algorithm:", bg="#f0f8ff").pack(anchor='w', padx=10, pady=(10, 0))
algo_var = tk.StringVar(value='sha256')
algo_dropdown = ttk.Combobox(root, textvariable=algo_var, values=sorted(hashlib.algorithms_guaranteed), state="readonly")
algo_dropdown.pack(padx=10, fill='x')

# Check button
tk.Button(root, text="🔎 Verify with Hashy", command=check_checksum, bg="#8ecae6", fg="black").pack(pady=15)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f8ff")
status_label.pack()

# Start the GUI
root.mainloop()
