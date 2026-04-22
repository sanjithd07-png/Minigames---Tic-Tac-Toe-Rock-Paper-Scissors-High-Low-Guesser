"""
Program: Play.py
Date: December 12, 2025
Programmer: Sanjith Diddla
Description: Play Button Clicked opens up this menu with a selection of mini games to play.
             Shows three game options: High/Low, Rock Paper Scissors, and Tic Tac Toe.

Note: This menu uses invisible clickable areas over the background image to navigate to different games.
      All three games were custom designed with pixel art backgrounds made in Canva.

Refferences: https://stackoverflow.com/questions/41656176/tkinter-make-a-part-of-image-clickable
             (For creating clickable areas on an image in Tkinter) This didn't help a lot but was a good starting point.
            Also, for the run_script function, I referred to AI to help with that to make it more efficient.

"""


# Import Statements
import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import pygame
import subprocess
import sys
 

# Window
window = Tk()
window.title("Play Menu Screen")
window.geometry("960x540")
window.resizable(False, False)


# Current Working Directory (For the Files and importing images)
current_dir = os.path.dirname(os.path.abspath(__file__))


# Pygame Background Music
pygame.mixer.init()
try:
    pygame.mixer.music.load(os.path.join(current_dir, "background.mp3"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)
except:
    print("Background music not found")

# Load click sound effect
try:
    click_sound = pygame.mixer.Sound(os.path.join(current_dir, "click.mp3"))
    click_sound.set_volume(1.0)  # Max volume
except:
    print("Click sound not found")
    click_sound = None


# Loading Image
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "playmenu.png")))
bg_label = tkinter.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Functions
def run_script(filename):
    script_path = os.path.join(current_dir, filename)
    subprocess.Popen([sys.executable, script_path])
    window.destroy()

def HL_clicked_action():
    run_script("HighLow.py")

def ttt_clicked_action():
    run_script("TTT.py")

def RRS_clicked_action():
    run_script("RRS.py")

def Main_clicked_action():
    run_script("Assignment4.py")

def exit_clicked_action():
    window.destroy()

def HL_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, HL_clicked_action)

def ttt_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, ttt_clicked_action)

def RRS_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, RRS_clicked_action)

def Main_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, Main_clicked_action)

def exit_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, exit_clicked_action)


# Function for invisible clickable areas
def clickable_area(event):
    x, y = event.x, event.y

    # High Low area
    if 265 <= x <= 265 + 205 and 130 <= y <= 130 + 150:
        HL_clicked()

    # Tic Tac Toe area
    if 488 <= x <= 488 + 205 and 132 <= y <= 132 + 150:
        ttt_clicked()

    # Rock Paper Scissors area
    if 268 <= x <= 268 + 205 and 293 <= y <= 293 + 150:
        RRS_clicked()

    # Main Menu area
    if 488 <= x <= 488 + 205 and 297 <= y <= 297 + 85:
        Main_clicked()

    # Exit area
    if 488 <= x <= 488 + 205 and 393 <= y <= 393 + 50:
        exit_clicked()

# Bind the left-clicks on the background to the clickable areas
bg_label.bind("<Button-1>", clickable_area)


# Mainloop
window.mainloop()