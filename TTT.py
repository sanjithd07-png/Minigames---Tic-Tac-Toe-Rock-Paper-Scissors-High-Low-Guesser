"""
Program: Tic Tac Toe
Date: December 12, 2025
Programmer: Sanjith Diddla
Description: Tic Tac Toe game with single player mode against an AI opponent and two player mode.

Note: This game implements a 3x3 grid using a 2D array to track the game board. The AI opponent 
      makes random moves for simplicity. The game checks for winning combinations after each move 
      and displays the winner or tie result.

References: Used concepts learned in class for 2D arrays and game logic.
            Used AI to help with the winning combination checking algorithm and the 2D array structure.

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
window.title("Tic Tac Toe")
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
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "TTT.png")))
bg_label = tkinter.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Game Variables
game_mode = ""  # "one_player" or "two_player"
board = [["", "", ""], ["", "", ""], ["", "", ""]]  # 2D Array for the game board
current_player = "X"  # X always goes first
game_active = False
p1_score = 0  # X score
p2_score = 0  # O score


# Score Labels
p1_score_label = Label(window, text="0", font=("Arial", 40, "bold"), 
                       bg="#bfebf4", fg="black", justify="center")
p1_score_label.place(x=50, y=265, width=60, height=50)

p2_score_label = Label(window, text="0", font=("Arial", 40, "bold"), 
                       bg="#bfebf4", fg="black", justify="center")
p2_score_label.place(x=127, y=265, width=60, height=50)

# print(f"Current player: {current_player}")  # Used this for testing

# Commentary Label (blue rectangle at bottom)
commentary_label = Label(window, text="Choose a game mode to start!", 
                         font=("Arial", 14, "bold"), bg="#00b6c9", fg="black")
commentary_label.place(x=250, y=443, width=460, height=30)


# Create 3x3 grid of buttons for Tic Tac Toe
# This part was tricky - took a while to figure out
button_grid = []
for row in range(3):
    button_row = []
    for col in range(3):
        btn = Button(window, text="", font=("Arial", 50, "bold"), 
                     bg="#c4e8e8", fg="black", relief="flat")
        # Position buttons in a 3x3 grid
        x_pos = 312 + (col * 115)
        y_pos = 91 + (row * 115)
        btn.place(x=x_pos, y=y_pos, width=95, height=95)
        button_row.append(btn)
    button_grid.append(button_row)


# Update Score Display
def update_scores():
    """Update the score labels on screen"""
    p1_score_label.config(text=str(p1_score))
    p2_score_label.config(text=str(p2_score))


# Reset Board Function
def reset_board():
    """Reset the game board"""
    global board, current_player, game_active
    
    # Reset the 2D array
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"
    game_active = True
    
    # Clear all buttons
    for row in range(3):
        for col in range(3):
            button_grid[row][col].config(text="", state="normal")
    
    # Update commentary
    if game_mode == "one_player":
        commentary_label.config(text="Your turn! Click any square to place X")
    elif game_mode == "two_player":
        commentary_label.config(text="Player X's turn! Click any square")


# Check Winner Function
def check_winner():
    """Check if there is a winner or tie"""
    
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            return board[row][0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    
    # Check for tie (board is full)
    is_full = True
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                is_full = False
                break
    
    if is_full:
        return "TIE"
    
    return None


# End Game Function
def end_game(winner):
    """Handle game end"""
    global game_active, p1_score, p2_score
    
    game_active = False
    
    # Disable all buttons
    for row in range(3):
        for col in range(3):
            button_grid[row][col].config(state="disabled")
    
    # Update scores and commentary
    if winner == "TIE":
        commentary_label.config(text="It's a Tie! Click REPLAY to play again")
    elif winner == "X":
        p1_score += 1
        update_scores()
        if game_mode == "one_player":
            commentary_label.config(text="You Win! X got three in a row!")
        else:
            commentary_label.config(text="Player X Wins! Three in a row!")
    elif winner == "O":
        p2_score += 1
        update_scores()
        if game_mode == "one_player":
            commentary_label.config(text="Computer Wins! O got three in a row!")
        else:
            commentary_label.config(text="Player O Wins! Three in a row!")


# AI Move Function (for single player)
def ai_move():
    """Computer makes a random move"""
    if not game_active:
        return
    
    # Find all empty spots
    empty_spots = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                empty_spots.append((row, col))
    
    # If there are empty spots, pick one randomly
    if empty_spots:
        row, col = random.choice(empty_spots)
        make_move(row, col)


# Make Move Function
def make_move(row, col):
    """Place a move on the board"""
    global current_player, game_active
    
    if not game_active:
        return
    
    # Check if spot is already taken
    if board[row][col] != "":
        return
    
    # Place the move
    board[row][col] = current_player
    button_grid[row][col].config(text=current_player)
    
    # Play click sound when move is made
    if click_sound:
        click_sound.play()
    
    # Check for winner
    winner = check_winner()
    if winner:
        end_game(winner)
        return
    
    # Switch players
    if current_player == "X":
        current_player = "O"
        if game_mode == "one_player":
            commentary_label.config(text="Computer's turn...")
            # AI makes move after short delay
            window.after(500, ai_move)
        else:
            commentary_label.config(text="Player O's turn! Click any square")
    else:
        current_player = "X"
        if game_mode == "one_player":
            commentary_label.config(text="Your turn! Click any square")
        else:
            commentary_label.config(text="Player X's turn! Click any square")


# Button Click Handler
def button_clicked(row, col):
    """Handle button clicks on the grid"""
    if not game_active:
        commentary_label.config(text="Choose a game mode to start!")
        return
    
    # In one player mode, only allow human (X) to click
    if game_mode == "one_player" and current_player == "O":
        return
    
    make_move(row, col)


# Bind click events to all buttons (keeping lambdas here since they were already in your code)
for row in range(3):
    for col in range(3):
        button_grid[row][col].config(command=lambda r=row, c=col: button_clicked(r, c))


# Game Mode Selection Functions
def one_player_clicked():
    """Start one player mode (vs Computer)"""
    if click_sound:
        click_sound.play()
    global game_mode, p1_score, p2_score
    game_mode = "one_player"
    p1_score = 0
    p2_score = 0
    update_scores()
    reset_board()
    commentary_label.config(text="One Player Mode! You are X, Computer is O")


def two_player_clicked():
    """Start two player mode"""
    if click_sound:
        click_sound.play()
    global game_mode, p1_score, p2_score
    game_mode = "two_player"
    p1_score = 0
    p2_score = 0
    update_scores()
    reset_board()
    commentary_label.config(text="Two Player Mode! Player X starts")


def replay_clicked():
    """Replay the current game mode"""
    if click_sound:
        click_sound.play()
    if game_mode == "":
        commentary_label.config(text="Choose a game mode first!")
    else:
        reset_board()


# Running the Different Py Files
def run_script(filename):
    """Function to run external Python scripts and close current window"""
    script_path = os.path.join(current_dir, filename)
    subprocess.Popen([sys.executable, script_path])
    window.destroy()

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
    
    # ONE PLAYER button
    elif 775 <= x <= 888 and 177 <= y <= 237:
        one_player_clicked()
    
    # REPLAY button
    elif 775 <= x <= 888 and 250 <= y <= 300:
        replay_clicked()
    
    # TWO PLAYER button
    elif 775 <= x <= 888 and 312 <= y <= 372:
        two_player_clicked()


# Bind clicks to background image
bg_label.bind("<Button-1>", clickable_area)


# Mainloop
window.mainloop()