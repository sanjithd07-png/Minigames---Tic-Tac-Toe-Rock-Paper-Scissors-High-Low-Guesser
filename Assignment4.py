"""
Program: Assignment 4
Date: December 12, 2025
Programmer: Sanjith Diddla
Description: Main Menu Screen with the Play, Help and Exit Buttons.  Includes a nice background theme music.  

Link to all of the custom made backgrounds: https://www.canva.com/design/DAG7IjN2bZQ/5FcxERcBpCpkp3EwYmWyuA/edit?utm_content=DAG7IjN2bZQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Refferences: For running the different python files when clicking the buttons, I used run_script function from this link: https://stackoverflow.com/questions/7067614/how-to-run-another-python-script-from-a-python-script and AI Help

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
import time
 

# Window
window = Tk()
window.title("Main Menu Screen")
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


# Loading Image (Main Menu)
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "MainMenu.png")))
bg_label = tkinter.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Running the Different Py Files
def run_script(filename):
    script_path = os.path.join(current_dir, filename)
    subprocess.Popen([sys.executable, script_path])
    window.destroy()


# Delayed action functions
def do_play_action():
    run_script("Play.py")

def do_help_action():
    run_script("help.py")

def do_exit_action():
    window.destroy()


# Play Button Function
def Play_Button():
    if click_sound:
        click_sound.play()
    window.after(500, do_play_action)


# Help Button Function
def Help_Button():
    if click_sound:
        click_sound.play()
    window.after(500, do_help_action)


# Exit Button Function
def Exit_Button():
    if click_sound:
        click_sound.play()
    window.after(500, do_exit_action)


# Makes the button area clickable but invisible
def button_area_clicked(event):
    x, y = event.x, event.y

    # Play button area
    if 385 <= x <= 542 and 250 <= y <= 308:
        Play_Button()

    # Help button area 
    if 385 <= x <= 542 and 323 <= y <= 383:
        Help_Button()

    # Exit button area
    if 385 <= x <= 542 and 398 <= y <= 458:
        Exit_Button()


bg_label.bind("<Button-1>", button_area_clicked)


# Mainloop
window.mainloop()