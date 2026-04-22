"""
Program: Rock Paper Scissors
Date: December 12, 2025
Programmer: Sanjith Diddla
Description: Rock Paper Scissors game with One Player (vs Computer) and Two Player modes.
Note: 

This game took a long time to do and a lot of thinking as I wanted to do the animation of the rock paper scissors game, which was quite hard to implement with tkinter.
To get the animation, I had to invdividually download 20 images from canva with one single image per frame but each one 5 degrees up and down to create a smooth animation effect.
After getting the images, I had to find a free Text to Speech website to generate the "Rock, Paper, Scissors, Shoot!" sound effect as I could not find any free sound effects online.
Then  I had to do some calculations to get the timing right for the animation to sync with the sound effect.
After a ton of trial and error, I've managed to make the animation, sound effects, game commentary, score system, and match history work as smooth as possible.
Thanks for the patience in reading this note and the inspiration from the turing project you showed me in class.

References: I took inspiration for the animation from the Turing Project you showed me in class.
            I also used ChatGPT to help me with some parts of the code, especially the animation loop system (animate_frame function).
            I also used AI to help me with the the pausing of the background music during the RRS sound effect.
            I also used AI to help me with the timinig delays with the window.after() function.

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
window.title("Rock Paper Scissors")
window.geometry("960x540")
window.resizable(False, False)


# Current Working Directory (For the Files and importing images)
current_dir = os.path.dirname(os.path.abspath(__file__))


# Pygame Background Music
pygame.mixer.init()
try:
    pygame.mixer.music.load(os.path.join(current_dir, "background.mp3"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.08)
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
bg_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "rrs.png")))
bg_label = tkinter.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Game Variables
game_mode = ""
p1_score = 0
p2_score = 0
current_player = 1
p1_choice = ""
p2_choice = ""
game_active = False
is_animating = False
match_history = []  # Array to store match results


# Score Labels (P1 and P2 scores on the left)
p1_score_label = Label(window, text="0", font=("Arial", 40, "bold"), 
                       bg="#bfebf4", fg="black", justify="center")
p1_score_label.place(x=50, y=265, width=60, height=50)

p2_score_label = Label(window, text="0", font=("Arial", 40, "bold"), 
                       bg="#bfebf4", fg="black", justify="center")
p2_score_label.place(x=127, y=265, width=60, height=50)


# Load Rock, Paper, Scissors images
try:
    rock_img = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "rock.png")).resize((150, 150)))
    paper_img = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "paper.png")).resize((150, 150)))
    scissors_img = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "scissors.png")).resize((150, 150)))
except:
    print("Could not load RPS images")
    rock_img = None
    paper_img = None
    scissors_img = None


# Load animation frames (1.png to 20.png)
animation_frames = []
try:
    for i in range(1, 21):
        frame = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, f"{i}.png")).resize((150, 150)))
        animation_frames.append(frame)
    print(f"Loaded {len(animation_frames)} animation frames")
except Exception as e:
    print(f"Could not load animation frames: {e}")


# Player One Display (shows choice image)
player_one_label = Label(window, bg="#ffffff")
player_one_label.place(x=264, y=210, width=150, height=150)


# Player Two Display (shows choice image)
player_two_label = Label(window, bg="#ffffff")
player_two_label.place(x=542, y=210, width=150, height=150)


# Commentary Label (blue rectangle at bottom)
commentary_label = Label(window, text="Choose a game mode to start!", 
                         font=("Arial", 12, "bold"), bg="#00b6c9", fg="black")
commentary_label.place(x=250, y=443, width=460, height=30)


# Running the Different Py Files
def run_script(filename):
    """Function to run external Python scripts and close current window"""
    script_path = os.path.join(current_dir, filename)
    subprocess.Popen([sys.executable, script_path])
    window.destroy()


# Update Score Display
def update_scores():
    # Updates the score display
    p1_score_label.config(text=str(p1_score))
    p2_score_label.config(text=str(p2_score))


# Reset Game Function
def reset_game():
    """Reset scores and game state"""
    global p1_score, p2_score, game_active, p1_choice, p2_choice, current_player, match_history
    p1_score = 0
    p2_score = 0
    p1_choice = ""
    p2_choice = ""
    current_player = 1
    game_active = True
    match_history = []
    update_scores()
    player_one_label.config(image="", text="")
    player_two_label.config(image="", text="")
    
    if game_mode == "one_player":
        commentary_label.config(text="Player 1: Choose Rock, Paper, or Scissors!")
    elif game_mode == "two_player":
        commentary_label.config(text="Player 1: Choose Rock, Paper, or Scissors!")


# Determine Winner Function
def determine_winner(choice1, choice2):
    """Determine the winner between two choices"""
    if choice1 == choice2:
        return 0  # Tie
    
    # Check all winning combinations
    if choice1 == "Rock":
        if choice2 == "Scissors":
            return 1  # Rock beats Scissors
        else:
            return 2  # Paper beats Rock
    
    elif choice1 == "Paper":
        if choice2 == "Rock":
            return 1  # Paper beats Rock
        else:
            return 2  # Scissors beats Paper
    
    elif choice1 == "Scissors":
        if choice2 == "Paper":
            return 1  # Scissors beats Paper
        else:
            return 2  # Rock beats Scissors


# Get Image for Choice
def get_choice_image(choice):
    """Return the image for a given choice"""
    if choice == "Rock":
        return rock_img
    elif choice == "Paper":
        return paper_img
    elif choice == "Scissors":
        return scissors_img
    return None


# Resume background music after delay
def resume_music():
    """Resume background music"""
    try:
        pygame.mixer.music.unpause()
    except:
        pass


# Animation System
def play_animation(p1_move, p2_move):
    """Play the rock-paper-scissors animation before revealing choices"""
    global is_animating
    
    # Check if animation frames are loaded
    if len(animation_frames) == 0:
        print("No animation frames, skipping to result")
        show_final_result(p1_move, p2_move)
        return
    
    is_animating = True
    
    # Pause background music and play RRS sound
    try:
        pygame.mixer.music.pause()
        rrs_sound = pygame.mixer.Sound(os.path.join(current_dir, "RRS SOUND.mp3"))
        rrs_sound.set_volume(1.0)
        rrs_sound.play()
    except Exception as e:
        print(f"Could not play RRS sound: {e}")
    
    # Start animation at loop 0, frame 0
    animate_frame(0, 0, p1_move, p2_move)


def animate_frame(loop_count, frame_index, p1_move, p2_move):
    """Display one frame of the animation"""
    global is_animating
    
    # Total 3 loops of 20 frames each
    if loop_count < 3:
        if frame_index < len(animation_frames):
            # Display current frame on both player displays
            current_frame = animation_frames[frame_index]
            player_one_label.config(image=current_frame, text="")
            player_one_label.image = current_frame
            player_two_label.config(image=current_frame, text="")
            player_two_label.image = current_frame
            
            # Calculate delay: 750ms per loop / 20 frames = 37.5ms per frame
            delay = 37
            
            # Schedule next frame
            window.after(delay, continue_animation, loop_count, frame_index + 1, p1_move, p2_move)
        else:
            # Finished one loop, start next loop
            window.after(37, continue_animation, loop_count + 1, 0, p1_move, p2_move)
    else:
        # Animation complete (3 loops done), show final result
        is_animating = False
        show_final_result(p1_move, p2_move)
        
        # Resume background music after a short delay
        window.after(500, resume_music)


def continue_animation(loop_count, frame_index, p1_move, p2_move):
    """Continue to next animation frame"""
    animate_frame(loop_count, frame_index, p1_move, p2_move)


def show_final_result(p1_move, p2_move):
    """Show the final result after animation"""
    global p1_score, p2_score, match_history
    
    # Show choice images on screen
    p1_img = get_choice_image(p1_move)
    p2_img = get_choice_image(p2_move)
    
    if p1_img and p2_img:
        player_one_label.config(image=p1_img, text="")
        player_one_label.image = p1_img
        player_two_label.config(image=p2_img, text="")
        player_two_label.image = p2_img
    else:
        # Fallback to text if images not loaded
        player_one_label.config(text=p1_move, font=("Arial", 20, "bold"), image="")
        player_two_label.config(text=p2_move, font=("Arial", 20, "bold"), image="")
    
    # Determine winner
    result = determine_winner(p1_move, p2_move)
    
    # Store match result in array
    match_history.append(result)
    
    # Update scores and display result
    if result == 0:
        commentary_label.config(text=f"It's a Tie! Both chose {p1_move}!")
    elif result == 1:
        p1_score += 1
        if game_mode == "one_player":
            commentary_label.config(text=f"You Win! {p1_move} beats {p2_move}!")
        else:
            commentary_label.config(text=f"Player 1 Wins! {p1_move} beats {p2_move}!")
    else:
        p2_score += 1
        if game_mode == "one_player":
            commentary_label.config(text=f"Computer Wins! {p2_move} beats {p1_move}!")
        else:
            commentary_label.config(text=f"Player 2 Wins! {p2_move} beats {p1_move}!")
    
    # Update score display
    update_scores()


# One Player Mode - Player makes a choice
def one_player_choice(choice):
    """Handle player choice in one player mode"""
    global game_active, is_animating
    
    if not game_active or is_animating:
        return
    
    # Player's choice
    player_choice = choice
    
    # Computer makes random choice
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)
    
    # Play animation then show result
    play_animation(player_choice, computer_choice)


# Reset commentary to Player 1's turn
def reset_to_player1():
    """Reset commentary to Player 1's turn"""
    commentary_label.config(text="Player 1: Choose Rock, Paper, or Scissors!")


# Two Player Mode - Players take turns
def two_player_choice(choice):
    """Handle player choices in two player mode"""
    global current_player, p1_choice, p2_choice, game_active, is_animating
    
    if not game_active or is_animating:
        return
    
    # Player 1's turn
    if current_player == 1:
        p1_choice = choice
        player_one_label.config(text="✓", font=("Arial", 50, "bold"), image="")
        commentary_label.config(text="Player 2: Choose Rock, Paper, or Scissors!")
        current_player = 2
    
    # Player 2's turn
    elif current_player == 2:
        p2_choice = choice
        player_two_label.config(text="✓", font=("Arial", 50, "bold"), image="")
        commentary_label.config(text="Get ready...")
        
        # Both players have chosen, play animation
        play_animation(p1_choice, p2_choice)
        
        # Reset for next round after animation completes
        current_player = 1
        window.after(5000, reset_to_player1)


# Handle Rock, Paper, Scissors button clicks
def rock_clicked():
    """Handle Rock button click"""
    if click_sound:
        click_sound.play()
    if game_mode == "one_player":
        one_player_choice("Rock")
    elif game_mode == "two_player":
        two_player_choice("Rock")
    else:
        commentary_label.config(text="Please choose a game mode first!")


def paper_clicked():
    """Handle Paper button click"""
    if click_sound:
        click_sound.play()
    if game_mode == "one_player":
        one_player_choice("Paper")
    elif game_mode == "two_player":
        two_player_choice("Paper")
    else:
        commentary_label.config(text="Please choose a game mode first!")


def scissors_clicked():
    """Handle Scissors button click"""
    if click_sound:
        click_sound.play()
    if game_mode == "one_player":
        one_player_choice("Scissors")
    elif game_mode == "two_player":
        two_player_choice("Scissors")
    else:
        commentary_label.config(text="Please choose a game mode first!")


# Game Mode Selection Functions
def one_player_clicked():
    """Start one player mode"""
    if click_sound:
        click_sound.play()
    global game_mode
    game_mode = "one_player"
    reset_game()
    commentary_label.config(text="One Player Mode! Choose Rock, Paper, or Scissors!")


def two_player_clicked():
    """Start two player mode"""
    if click_sound:
        click_sound.play()
    global game_mode
    game_mode = "two_player"
    reset_game()
    commentary_label.config(text="Two Player Mode! Player 1 starts!")


def replay_clicked():
    """Replay the current game mode"""
    if click_sound:
        click_sound.play()
    if game_mode == "":
        commentary_label.config(text="Choose a game mode first!")
    else:
        reset_game()


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
    
    # ROCK button
    elif 283 <= x <= 393 and 392 <= y <= 422:
        rock_clicked()
    
    # PAPER button
    elif 423 <= x <= 533 and 392 <= y <= 422:
        paper_clicked()
    
    # SCISSORS button
    elif 567 <= x <= 677 and 392 <= y <= 422:
        scissors_clicked()
    
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