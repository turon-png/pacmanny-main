import copy
import pygame
import math
import sys
import os
import welcome  # Importing welcome.py
from board import boards, easy_boards  # Import both normal and easy mode boards

# Ensure Python recognizes the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60

# Load a better-looking font
font = pygame.font.Font('freesansbold.ttf', 30)

# Change background color to white
screen.fill((255, 255, 255))

# Display the welcome screen
welcome.display_welcome_message(screen, font)
pygame.time.delay(500)

# Wait for user input to start the game
if not welcome.wait_for_user_input():
    pygame.quit()
    quit()

# Select difficulty level
difficulty = welcome.select_difficulty(screen, font)

# Adjust game speed and board based on difficulty
if difficulty == "Easy":
    player_speed = 2
    ghost_speeds = [1]  # Only one ghost, slower speed
    level = copy.deepcopy(easy_boards)  # Load reduced obstacles
    single_ghost = True  # Indicate only one ghost
else:
    player_speed = 2 if difficulty == "Medium" else 3
    ghost_speeds = [2, 2, 2, 2] if difficulty == "Medium" else [3, 3, 3, 3]
    level = copy.deepcopy(boards)
    single_ghost = False

color = 'blue'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
counter = 0
flicker = False
turns_allowed = [False, False, False, False]
direction_command = 0
score = 0
powerup = False
power_counter = 0
eaten_ghost = False
targets = [(player_x, player_y)]
blinky_dead = False
blinky_box = False
moving = False
startup_counter = 0
lives = 3
game_over = False
game_won = False
