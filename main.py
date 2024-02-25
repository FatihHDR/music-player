import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import os
import threading
import tkinter as tk
import pygame.mixer_music as music
import pygame
import random

folder_path=r"C:\Users\vyoms\OneDrive\Desktop\Projects\Music\Songs" # Enter Default Folder Path

def get_song_list(folder_path):
    songs = []
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            songs.append(file)
    return songs
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        song_listbox.delete(0, "end")
        songs = get_song_list(folder_path)
        for song in songs:
            song_listbox.insert("end", song)
        thread = threading.Thread(target=monitor_folder_changes, args=(folder_path,))
        thread.daemon = True
        thread.start()


def monitor_folder_changes(folder_path):
    songs = get_song_list(folder_path)
    while True:
        time.sleep(5)
        new_songs = get_song_list(folder_path)
        if new_songs != songs:
            song_listbox.delete(0, "end")
            for song in new_songs:
                song_listbox.insert("end", song)
            songs = new_songs


def play_selected_song(event):
    global folder_path
    global song_path
    selected_song = song_listbox.get(song_listbox.curselection())
    if selected_song:
        song_path = os.path.join(folder_path, selected_song)
        mixer.init()
        mixer.music.load(song_path)
        mixer.music.play()
        if paused:
            mixer.music.pause()
def check_song_end():
    while True:
        if paused:
            continue
        elif not mixer.music.get_busy():
            play_next_song()
        time.sleep(1)
def toggle_play_pause():
    global paused
    if paused:
        mixer.init()
        mixer.music.unpause()
        paused = False
        play_pause_button.configure(image=pause_image)
    else:
        mixer.init()
        mixer.music.pause()
        paused = True
        play_pause_button.configure(image=play_image)
def play_next_song():
    if song_listbox.curselection():
        next_song = song_listbox.curselection()[0]
        if next_song== song_listbox.size()-1:
            song_listbox.selection_clear(0, "end")
            song_listbox.activate(0)
            song_listbox.selection_set(0, last=None)
            play_selected_song(None)
        else:
            next_song = song_listbox.curselection()[0]+1
            song_listbox.selection_clear(0, "end")
            song_listbox.activate(next_song)
            song_listbox.selection_set(next_song, last=None)
            play_selected_song(None)
def play_prev_song():
    next_song = song_listbox.curselection()[0]
    if next_song == 0:
        song_listbox.selection_clear(0, "end")
        song_listbox.activate(song_listbox.size()-1)
        song_listbox.selection_set(song_listbox.size()-1, last=None)
        play_selected_song(None)
    else:
        next_song = song_listbox.curselection()[0] - 1
        song_listbox.selection_clear(0, "end")
        song_listbox.activate(next_song)
        song_listbox.selection_set(next_song, last=None)
        play_selected_song(None)
def play_random_song():
    if song_listbox.size() > 0:
        random_index = random.randint(0, song_listbox.size() - 1)
        song_listbox.selection_clear(0, "end")
        song_listbox.activate(random_index)
        song_listbox.selection_set(random_index, last=None)
        play_selected_song(None)


root = Tk()
screen_width = root.winfo_screenwidth()
root.title("Music Player")
root.geometry("780x590+100+10")
root.configure(background="#333333")
# root.resizable(0,0)


# Create a PanedWindow widget
paned_window = PanedWindow(root, orient="horizontal", sashrelief="raised", sashwidth=5)
paned_window.pack(fill="both", expand=True)

# Songs Structure
left_frame = Frame(paned_window, bg="#d4faea", relief="solid", padx=10, pady=10)
right_frame = Frame(paned_window, bg="white", relief="solid", padx=10, pady=10)

# Song List (Left Frame)
song_list_frame = Frame(left_frame, bg="#d4faea")
song_list_frame.pack(fill="both", expand=True)

# add heading to  side frame with division
heading = Label(song_list_frame, text="List of Songs", font=("arial", 15, "bold"), bg="#d4faea")
heading.pack(anchor="center", pady=10)

# add listbox to side frame
song_listbox = Listbox(song_list_frame, bg="white", width=50, height=800, selectmode="single", highlightthickness=0, )
song_listbox.pack(fill="both", anchor="center", pady=(50, 20), side="top")

#Default songs

# songs
default_songs=get_song_list(folder_path)
for si in default_songs:
    song_listbox.insert("end",si)
thread = threading.Thread(target=monitor_folder_changes, args=(folder_path,))
thread.daemon = True
thread.start()

# add scrollbar to side frame
scrollbar = Scrollbar(song_list_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")
# Configure the scrollbar
song_listbox.config(yscrollcommand=scrollbar.set)

# Add the songs from the playlist to the listbox
browse_text = Label(song_list_frame, text="Select From Device ", font=("Times New Roman", 11, "bold"), bg="#FFFFFF")
browse_text.pack(anchor="center", side="right", pady=80)

browse_button = Button(song_list_frame, text="Browse", font=("Times New Roman", 12), command=select_folder, width=10)
browse_button.place(x=0, y=70, width=100, height=30)
# Add the frames to the PanedWindow
paned_window.add(left_frame)
paned_window.add(right_frame)

# Set the initial sizes of the frames
paned_window.paneconfig(left_frame, minsize=150)
paned_window.paneconfig(right_frame, minsize=400)

# Bind the select event of the listbox to the play_selected_song function
song_listbox.bind("<<ListboxSelect>>", play_selected_song)

# Song Playing Panel (Right Frame)
# Bar with buttons (Right Frame)
button_frame = Frame(right_frame, bg="#d4faea")
button_frame.pack(fill="x", side="bottom", ipady=50, pady=20)
paused = True



# Load the images for the buttons
pause_image = tk.PhotoImage(file=r"Images\pause1.png")
play_image = tk.PhotoImage(file=r"Images\play1.png")

# Play/Pause Button
play_pause_button = tk.Label(button_frame, image=play_image, borderwidth=0, highlightthickness=0, cursor="hand2",
                             bg="#d4faea")
play_pause_button.pack(side="left", padx=10, pady=10)
play_pause_button.bind("<Button-1>", lambda event: toggle_play_pause())
play_pause_button.pack_propagate(False)
play_pause_button.place(relx=0.5, rely=0.5, anchor="center")


# Play Next Button

# Loading Image for the button
next_image = tk.PhotoImage(file=r"Images\nex.png")

play_next_button = tk.Label(button_frame, image=next_image, borderwidth=0, highlightthickness=0, cursor="hand2",
                            bg="#d4faea")
play_next_button.pack(side="left", padx=10, pady=10)
play_next_button.bind("<Button-1>", lambda event: play_next_song())
play_next_button.pack_propagate(False)
play_next_button.place(relx=0.6, rely=0.5, anchor="center")


# Play Previous  Button

# Loading Image for the button
prev_image = tk.PhotoImage(file=r"Images/prev.png")

play_prev_button = tk.Label(button_frame, image=prev_image, borderwidth=0, highlightthickness=0, cursor="hand2",
                            bg="#d4faea")
play_prev_button.pack(side="left", padx=10, pady=10)
play_prev_button.bind("<Button-1>", lambda event: play_prev_song())
play_prev_button.pack_propagate(False)
play_prev_button.place(relx=0.4, rely=0.5, anchor="center")


# Volume Slider
def set_volume(event):
    volume = volume_slider.get()
    mixer.init()
    mixer.music.set_volume(volume / 100)


volume_slider = Scale(button_frame, from_=0, to=100, orient="horizontal", bg="#d4faea", fg="#333333",
                      highlightthickness=0, bd=0, command=set_volume, length=100, width=20, variable="volume")
volume_slider.set(50)
volume_slider.pack_propagate(False)
volume_slider.place(relx=0.8, rely=0.4, anchor="center")

# Volume Label
volume_label = Label(button_frame, text="Volume", bg="#d4faea", fg="#333333", font=("arial", 10, "bold"))
volume_label.pack_propagate(False)
volume_label.place(relx=0.8, rely=0.7, anchor="center")

image_frame = Frame(right_frame, bg="#FFFFFF")
image_frame.pack(fill="both", expand=True)

# Load the PNG image
image_path = r"Images\VS & Co..png"  # Replace with the path to your PNG image
image = PhotoImage(file=image_path)

# Create a label to display the image
image_label = Label(image_frame, image=image, bg="#FFFFFF")
image_label.pack(anchor="center", padx=10, pady=10)

# Play Random Song

# Load the image for the play random button
random_image = tk.PhotoImage(file=r"Images\random.png")

play_random_button = tk.Label(button_frame, image=random_image, borderwidth=0, highlightthickness=0,
                              cursor="hand2", bg="#d4faea")
play_random_button.pack(side="left", padx=10, pady=10)
play_random_button.bind("<Button-1>", lambda event: play_random_song())
play_random_button.pack_propagate(False)
play_random_button.place(relx=0.2, rely=0.5, anchor="center")

mixer.init()
thread = threading.Thread(target=check_song_end)
thread.daemon = True
thread.start()


root.mainloop()

