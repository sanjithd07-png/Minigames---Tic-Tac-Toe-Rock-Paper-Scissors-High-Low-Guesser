"""
Program: help.py
Date: December 12, 2025
Programmer: Sanjith Diddla
Description: Help Button Clicked takes you to the help screen which explains how to play all three games
             and how to navigate the program.

Note: This screen provides instructions for Rock/Paper/Scissors, High/Low, and Tic Tac Toe games.
      The help menu uses the same background music and navigation system as other screens for consistency.
      
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
window.tk.call("tk", "scaling", 1.0)
window.title("Help Menu Screen")
window.geometry("559x774")
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
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "helpmenu.png")))
bg_label = tkinter.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Functions
def run_script(filename):
    script_path = os.path.join(current_dir, filename)
    subprocess.Popen([sys.executable, script_path])
    window.destroy()

def main_clicked_action():
    run_script("Assignment4.py")

def exit_clicked_action():
    window.destroy()

def main_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, main_clicked_action)

def exit_clicked():
    if click_sound:
        click_sound.play()
    window.after(500, exit_clicked_action)


# Function for clickable areas
def clickable_area(event):
    x, y = event.x, event.y

    # MENU button area 
    if 19 <= x <= 19 + 88 and 363 <= y <= 363 + 35:
        main_clicked()

    # EXIT button area 
    if 445 <= x <= 445 + 88 and 363 <= y <= 363 + 35:
        exit_clicked()

# Bind the left-clicks on the background to clickable areas
bg_label.bind("<Button-1>", clickable_area)


# Mainloop
window.mainloop()