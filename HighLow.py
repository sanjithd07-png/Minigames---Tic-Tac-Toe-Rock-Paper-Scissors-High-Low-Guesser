"""
Program: High Low Guessing Game
Date: December 12, 2025
Programmer: Sanjith Diddla
Description: High Low Guessing Game with three difficulty levels.
             Easy: 1-20 (unlimited guesses)
             Medium: 1-100 (10 guesses)
             Hard: 1-1000 (3 guesses)

Note: This mini game was the easiest of the 3 games to implement as I've already had experience creating 
      this game previously in my Assignment 1 project. The game uses arrays to store all the guesses made 
      by the player, and this information is displayed at the end of the game when you guess correctly or 
      run out of guesses. I also implemented error handling to check for invalid inputs, out of range guesses, 
      and duplicate guesses to make the game more user-friendly.

References: This game builds upon my previous work from Assignment 1 where I first created a text-based version.
            The GUI implementation and array tracking features are my own work based on concepts learned in class.
            I have used AI for the current working directory so it takes files from the same folder as this file.  I've used this in my other .py files as well in this assignment.  
            I've used a little bit of AI help to optimize some of error handling structure.  What I mean is for example the try/except for the Value Errors like checking for empty input and duplicate guesses.  

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
from tkinter import font as tkfont

 

# Window
window = Tk()
window.title("High Low Game")
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
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "HILOW.png")))
bg_label = tkinter.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Game Variables (using arrays and variables to track game state)
game_active = False
secret_number = 0
guess_count = 0
max_guesses = 0
min_range = 0
max_range = 0
difficulty = ""
guesses_list = []  # 1D Array to store all guesses


# Text Entry Box for guessing (positioned in the white square)
guess_entry = Entry(window, font=("Arial", 30), justify="center", bg="#f2fcfc", fg="black")
guess_entry.place(x=415, y=218, width=100, height=100)


# Commentary Label (long blue rectangle at bottom)
commentary_label = Label(window, text="Select a difficulty to start!", 
                         font=("Arial", 16, "bold"), bg="#00b6c9", fg="black")
commentary_label.place(x=278, y=392, width=380, height=35)


# Difficulty Display Label (shorter blue rectangle)
difficulty_label = Label(window, text="", font=("Arial", 12, "bold"), 
                         bg="#00b6c9", fg="black")
difficulty_label.place(x=355, y=442, width=220, height=30)


# Guesses Remaining Label (left side)
guesses_label = Label(window, text="", font=("Arial", 55, "bold"), 
                      bg="#bfebf4", fg="black", justify="center")
guesses_label.place(x=79, y=245, width=80, height=80)


# Running the Different Py Files
def run_script(filename):
    """Function to run external Python scripts and close current window"""
    script_path = os.path.join(current_dir, filename)
    subprocess.Popen([sys.executable, script_path])
    window.destroy()


# Start Game Function (uses decision statements to set difficulty)
def start_game(level):
    """Initialize game variables based on difficulty level selected"""
    global game_active, secret_number, guess_count, max_guesses
    global min_range, max_range, difficulty, guesses_list
    
    game_active = True
    guess_count = 0
    guesses_list = []  # Reset the guesses array
    
    # Decision statements to set game parameters
    if level == "easy":
        min_range = 1
        max_range = 20
        max_guesses = 999  # Unlimited (high number)
        difficulty = "Easy"
        guesses_label.config(text="∞")
        
    elif level == "medium":
        min_range = 1
        max_range = 100
        max_guesses = 10
        difficulty = "Medium"
        guesses_label.config(text=f"{max_guesses}")
        
    elif level == "hard":
        min_range = 1
        max_range = 1000
        max_guesses = 3
        difficulty = "Hard"
        guesses_label.config(text=f"{max_guesses}")
    
    # Generate random secret number
    secret_number = random.randint(min_range, max_range)
    
    # Update labels
    difficulty_label.config(text=f"Difficulty: {difficulty} ({min_range}-{max_range})")
    commentary_label.config(text=f"Guess a number between {min_range} and {max_range}!")
    
    # Clear entry box and set focus
    guess_entry.delete(0, END)
    guess_entry.focus()
    
    #print(f"DEBUG: Secret number is {secret_number}")  # This was used for testing


# Process Guess Function (includes error handling and loops logic)
def process_guess():
    """Process the player's guess with error handling"""
    global guess_count, game_active, guesses_list
    
    # Check if game is active
    if not game_active:
        messagebox.showwarning("No Game Active", "Please select a difficulty level first!")
        return
    
    # Get the guess from entry box
    guess_text = guess_entry.get().strip()
    
    # Error handling - check if input is empty
    if guess_text == "":
        commentary_label.config(text="Please enter a number!")
        return
    
    # Error handling - check if input is a valid number
    try:
        guess = int(guess_text)
    except ValueError:
        commentary_label.config(text="Invalid input! Please enter a number!")
        guess_entry.delete(0, END)
        return
    
    # Error handling - check if guess is in valid range
    if guess < min_range or guess > max_range:
        commentary_label.config(text=f"Guess must be between {min_range} and {max_range}!")
        guess_entry.delete(0, END)
        return
    
    # Check if guess was already made (prevents duplicate guesses)
    if guess in guesses_list:
        commentary_label.config(text=f"You already guessed {guess}! Try a different number!")
        guess_entry.delete(0, END)
        return
    
    # Add guess to array and increment counter
    guesses_list.append(guess)
    guess_count += 1
    
    # Update guesses remaining (if not unlimited)
    if difficulty != "Easy":
        guesses_remaining = max_guesses - guess_count
        guesses_label.config(text=f"{guesses_remaining}")
    
    # Decision statements - check if guess is correct
    if guess == secret_number:
        # WIN CONDITION
        game_active = False
        commentary_label.config(text=f"🎉 Correct! You guessed it in {guess_count} tries!")
        
        # Display all guesses made
        guesses_str = ", ".join(map(str, guesses_list))
        messagebox.showinfo("You Win!", 
                           f"Congratulations! You found the number!\n\n"
                           f"Number: {secret_number}\n"
                           f"Total Guesses: {guess_count}\n"
                           f"Your Guesses: {guesses_str}")
        
    elif guess < secret_number:
        # Guess is too low
        commentary_label.config(text=f"{guess} is too low! Try a higher number!")
        guess_entry.delete(0, END)
        
    else:
        # Guess is too high
        commentary_label.config(text=f"{guess} is too high! Try a lower number!")
        guess_entry.delete(0, END)
    
    # Check if player ran out of guesses (loop termination condition)
    if guess_count >= max_guesses and guess != secret_number and difficulty != "Easy":
        # LOSE CONDITION
        game_active = False
        commentary_label.config(text=f"Game Over! The number was {secret_number}!")
        
        guesses_str = ", ".join(map(str, guesses_list))
        messagebox.showinfo("Game Over", 
                           f"You ran out of guesses!\n\n"
                           f"The number was: {secret_number}\n"
                           f"Your Guesses: {guesses_str}")


# Action functions for delayed execution
def Help_Button_action():
    run_script("help.py")

def Exit_Button_action():
    window.destroy()

def menu_clicked_action():
    run_script("Assignment4.py")


# Button Functions
def Help_Button():
    """Open help screen"""
    if click_sound:
        click_sound.play()
    window.after(500, Help_Button_action)


def Exit_Button():
    """Exit the game"""
    if click_sound:
        click_sound.play()
    window.after(500, Exit_Button_action)


def menu_clicked(): 
    """Return to main menu"""
    if click_sound:
        click_sound.play()
    window.after(500, menu_clicked_action)


def easy_clicked():
    """Start easy mode"""
    if click_sound:
        click_sound.play()
    start_game("easy")


def medium_clicked():
    """Start medium mode"""
    if click_sound:
        click_sound.play()
    start_game("medium")


def hard_clicked():
    """Start hard mode"""
    if click_sound:
        click_sound.play()
    start_game("hard")


# Bind Enter key to submit guess (additional user interaction)
def on_enter_key(event):
    """Allow player to press Enter to submit guess"""
    process_guess()


guess_entry.bind("<Return>", on_enter_key)


# Clickable areas function
def clickable_area(event):
    """Handle clicks on invisible button areas"""
    x, y = event.x, event.y

    # HELP button
    if 58 <= x <= 178 and 101 <= y <= 148:
        Help_Button()

    # EXIT button
    elif 770 <= x <= 890 and 424 <= y <= 471:
        Exit_Button()

    # MENU button
    elif 58 <= x <= 178 and 424 <= y <= 471:
        menu_clicked()

    # EASY button
    elif 770 <= x <= 890 and 180 <= y <= 234:
        easy_clicked()

    # MEDIUM button
    elif 772 <= x <= 892 and 245 <= y <= 305:
        medium_clicked()

    # HARD button
    elif 770 <= x <= 890 and 316 <= y <= 370:
        hard_clicked()
    
    # SUBMIT button (long blue rectangle area)
    elif 250 <= x <= 710 and 395 <= y <= 435:
        if click_sound:
            click_sound.play()
        process_guess()


# Bind clicks to background image
bg_label.bind("<Button-1>", clickable_area)


# Mainloop
window.mainloop()