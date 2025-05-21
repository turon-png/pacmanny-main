import pygame
import time
import os
import csv
import random

# Initialize pygame
pygame.init()

# Get the directory where the script is running
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
HIGHSCORE_PATH = os.path.join(SCRIPT_DIR, "highscore.csv")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def create_pixel_background(width, height):
    """Create a pixel-style background surface"""
    surface = pygame.Surface((width, height))
    surface.fill(BLACK)
    
    # Add random colored pixels for a retro feel
    for _ in range(2000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        color = random.choice([(50, 50, 50), (20, 20, 20), (30, 30, 30)])
        surface.set_at((x, y), color)
    
    # Add some grid lines
    for x in range(0, width, 20):
        pygame.draw.line(surface, (20, 20, 20), (x, 0), (x, height), 1)
    for y in range(0, height, 20):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (width, y), 1)
    
    return surface

def load_high_score():
    """Load the high score and player name from CSV file."""
    try:
        if not os.path.exists(HIGHSCORE_PATH):
            return "None", 0
            
        with open(HIGHSCORE_PATH, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                # Check if first row is header
                first_row = next(reader)
                if len(first_row) >= 2 and first_row[0] == "PlayerName" and first_row[1] == "Score":
                    # Header exists, read next row for data
                    data_row = next(reader)
                else:
                    # No header, use first row as data
                    data_row = first_row
                
                if len(data_row) >= 2:
                    return data_row[0], int(data_row[1])
            except StopIteration:
                pass
        return "None", 0
    except Exception as e:
        print(f"Error loading high score: {e}")
        return "None", 0

def load_all_high_scores():
    """Load all high scores and player names from CSV file, sorted descending by score."""
    scores = []
    try:
        if not os.path.exists(HIGHSCORE_PATH):
            return scores
        with open(HIGHSCORE_PATH, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            start_index = 0
            if rows and rows[0][0] == "PlayerName" and rows[0][1] == "Score":
                start_index = 1
            for row in rows[start_index:]:
                if len(row) >= 2:
                    try:
                        scores.append((row[0], int(row[1])))
                    except ValueError:
                        pass
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
    except Exception as e:
        print(f"Error loading all high scores: {e}")
        return scores

def save_high_score(name, score):
    """Save the high score and player name to CSV file."""
    try:
        scores = {}
        # Read existing scores if file exists
        if os.path.exists(HIGHSCORE_PATH):
            with open(HIGHSCORE_PATH, "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                # Check if header exists
                start_index = 0
                if rows and rows[0][0] == "PlayerName" and rows[0][1] == "Score":
                    start_index = 1
                for row in rows[start_index:]:
                    if len(row) >= 2:
                        try:
                            player_name = row[0]
                            player_score = int(row[1])
                            # Keep the highest score per player
                            if player_name not in scores or player_score > scores[player_name]:
                                scores[player_name] = player_score
                        except ValueError:
                            pass
        # Update with new score if higher
        if name not in scores or score > scores[name]:
            scores[name] = score
        # Sort scores descending by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        # Write back to file with header
        with open(HIGHSCORE_PATH, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName", "Score"])
            for entry in sorted_scores:
                writer.writerow([entry[0], entry[1]])
        # Clean duplicates after saving
        remove_exact_duplicate_rows()
        clean_duplicate_scores()
        return True
    except Exception as e:
        print(f"Error saving high score: {e}")
        return False

def clean_duplicate_scores():
    """Remove duplicate player scores in the CSV file, keeping only the highest score per player."""
    try:
        scores = {}
        original_names = {}
        if not os.path.exists(HIGHSCORE_PATH):
            return False
        with open(HIGHSCORE_PATH, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            start_index = 0
            if rows and rows[0][0] == "PlayerName" and rows[0][1] == "Score":
                start_index = 1
            for row in rows[start_index:]:
                if len(row) >= 2:
                    try:
                        player_name_raw = row[0]
                        player_name = player_name_raw.strip().lower()
                        player_score = int(row[1])
                        if player_name not in scores or player_score > scores[player_name]:
                            scores[player_name] = player_score
                            original_names[player_name] = player_name_raw.strip()
                    except ValueError:
                        pass
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        with open(HIGHSCORE_PATH, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName", "Score"])
            for player_name, score in sorted_scores:
                writer.writerow([original_names[player_name], score])
        return True
    except Exception as e:
        print(f"Error cleaning duplicate scores: {e}")
        return False

def remove_exact_duplicate_rows():
    """Remove exact duplicate rows (player name and score) from the CSV file."""
    try:
        if not os.path.exists(HIGHSCORE_PATH):
            return False
        with open(HIGHSCORE_PATH, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        start_index = 0
        if rows and rows[0][0] == "PlayerName" and rows[0][1] == "Score":
            start_index = 1
        seen = set()
        unique_rows = []
        for row in rows[start_index:]:
            if len(row) >= 2:
                player_name = row[0].strip().lower()
                try:
                    player_score = int(row[1])
                except ValueError:
                    continue
                key = (player_name, player_score)
                if key not in seen:
                    seen.add(key)
                    unique_rows.append(row)
        with open(HIGHSCORE_PATH, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName", "Score"])
            for row in unique_rows:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error removing exact duplicate rows: {e}")
        return False

def draw_pixel_border(surface, rect, color, thickness=2):
    """Draw a pixel-style border around a rectangle"""
    # Top border
    pygame.draw.rect(surface, color, (rect.x, rect.y, rect.width, thickness))
    # Bottom border
    pygame.draw.rect(surface, color, (rect.x, rect.y + rect.height - thickness, rect.width, thickness))
    # Left border
    pygame.draw.rect(surface, color, (rect.x, rect.y, thickness, rect.height))
    # Right border
    pygame.draw.rect(surface, color, (rect.x + rect.width - thickness, rect.y, thickness, rect.height))
    
    # Add pixel-style corners
    corner_size = 10
    # Top-left
    pygame.draw.rect(surface, color, (rect.x, rect.y, corner_size, thickness))
    pygame.draw.rect(surface, color, (rect.x, rect.y, thickness, corner_size))
    # Top-right
    pygame.draw.rect(surface, color, (rect.x + rect.width - corner_size, rect.y, corner_size, thickness))
    pygame.draw.rect(surface, color, (rect.x + rect.width - thickness, rect.y, thickness, corner_size))
    # Bottom-left
    pygame.draw.rect(surface, color, (rect.x, rect.y + rect.height - thickness, corner_size, thickness))
    pygame.draw.rect(surface, color, (rect.x, rect.y + rect.height - corner_size, thickness, corner_size))
    # Bottom-right
    pygame.draw.rect(surface, color, (rect.x + rect.width - corner_size, rect.y + rect.height - thickness, corner_size, thickness))
    pygame.draw.rect(surface, color, (rect.x + rect.width - thickness, rect.y + rect.height - corner_size, thickness, corner_size))

def get_player_name(screen, font):
    input_text = ''
    active = True
    cursor_visible = True
    cursor_timer = 0

    high_scorer, high_score = load_high_score()
    all_scores = load_all_high_scores()
    
    # Create pixel background
    background = create_pixel_background(screen.get_width(), screen.get_height())
    
    # Create a retro font
    try:
        retro_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 36)
        title_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 48)
    except:
        retro_font = pygame.font.SysFont('courier', 36, bold=True)
        title_font = pygame.font.SysFont('courier', 48, bold=True)

    while active:
        # Draw the background
        screen.blit(background, (0, 0))
        
        # Add some animated pixels for effect
        for _ in range(5):
            x = random.randint(0, screen.get_width()-1)
            y = random.randint(0, screen.get_height()-1)
            pygame.draw.circle(screen, YELLOW, (x, y), 1)

        # Title with shadow effect
        title = title_font.render("PAC-MAN", True, BLUE)
        title_shadow = title_font.render("PAC-MAN", True, (50, 50, 150))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 80))
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)

        # High Score
        high_score_text = retro_font.render(f"High Score: {high_score}", True, YELLOW)
        high_score_shadow = retro_font.render(f"High Score: {high_score}", True, (100, 100, 0))
        high_score_rect = high_score_text.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(high_score_shadow, (high_score_rect.x + 2, high_score_rect.y + 2))
        screen.blit(high_score_text, high_score_rect)
        
        high_scorer_text = retro_font.render(f"by {high_scorer}", True, WHITE)
        high_scorer_rect = high_scorer_text.get_rect(center=(screen.get_width() // 2, 190))
        screen.blit(high_scorer_text, high_scorer_rect)

        # Display top 5 ranks with improved UI
        ranks_box_width = 500
        ranks_box_height = 200
        ranks_box_x = (screen.get_width() - ranks_box_width) // 2
        ranks_box_y = 230
        ranks_box_rect = pygame.Rect(ranks_box_x, ranks_box_y, ranks_box_width, ranks_box_height)
        
        # Draw box with pixel border
        pygame.draw.rect(screen, (20, 50, 50), ranks_box_rect, border_radius=5)
        draw_pixel_border(screen, ranks_box_rect, YELLOW, 3)
        
        # Leaderboard title
        leader_title = retro_font.render("LEADERBOARD", True, PINK)
        leader_rect = leader_title.get_rect(center=(screen.get_width() // 2, ranks_box_y + 20))
        screen.blit(leader_title, leader_rect)

        y_offset = ranks_box_y + 60
        rank = 1
        for name, sc in all_scores[:5]:
            rank_text = retro_font.render(f'{rank}. {name[:10]:<10} {sc:>5}', True, WHITE)
            rank_rect = rank_text.get_rect(midleft=(ranks_box_x + 40, y_offset))
            screen.blit(rank_text, rank_rect)
            y_offset += 35
            rank += 1

        # Input box
        box_width = 500
        box_height = 60
        input_box_rect = pygame.Rect((screen.get_width() - box_width) // 2, 500, box_width, box_height)
        pygame.draw.rect(screen, (30, 30, 30), input_box_rect, border_radius=5)
        draw_pixel_border(screen, input_box_rect, YELLOW, 3)

        prompt = retro_font.render("ENTER YOUR NAME:", True, WHITE)
        prompt_shadow = retro_font.render("ENTER YOUR NAME:", True, (100, 100, 100))
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 440))
        screen.blit(prompt_shadow, (prompt_rect.x + 2, prompt_rect.y + 2))
        screen.blit(prompt, prompt_rect)

        input_display = retro_font.render(input_text + ("|" if cursor_visible else ""), True, YELLOW)
        input_rect = input_display.get_rect(center=input_box_rect.center)
        screen.blit(input_display, input_rect)

        pygame.display.flip()

        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = input_text.strip() if input_text.strip() else "Player"
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 12:  # Limit name length
                        input_text += event.unicode

def display_welcome_message(screen, font, player_name):
    text_color = YELLOW
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(BLACK)

    # Create retro font
    try:
        retro_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 36)
        title_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 48)
    except:
        retro_font = pygame.font.SysFont('courier', 36, bold=True)
        title_font = pygame.font.SysFont('courier', 48, bold=True)

    welcome_text = retro_font.render(f"WELCOME {player_name.upper()}!", True, text_color)
    start_text = retro_font.render("PRESS ENTER TO START", True, WHITE)
    quit_text = retro_font.render("OR Q TO QUIT", True, WHITE)

    welcome_rect = welcome_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))

    # Create background
    background = create_pixel_background(screen.get_width(), screen.get_height())
    screen.blit(background, (0, 0))

    # Draw Pac-Man character
    pacman_radius = 50
    pacman_x = screen.get_width() // 2
    pacman_y = screen.get_height() // 3
    pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), pacman_radius)
    
    # Draw Pac-Man mouth
    mouth_angle = 0.4  # Radians
    pygame.draw.polygon(screen, BLACK, [
        (pacman_x, pacman_y),
        (pacman_x + pacman_radius * pygame.math.Vector2(1, 0).rotate(30).x, 
         pacman_y + pacman_radius * pygame.math.Vector2(1, 0).rotate(30).y),
        (pacman_x + pacman_radius * pygame.math.Vector2(1, 0).rotate(-30).x, 
         pacman_y + pacman_radius * pygame.math.Vector2(1, 0).rotate(-30).y)
    ])

    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(255 - alpha)
        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), pacman_radius)
        pygame.draw.polygon(screen, BLACK, [
            (pacman_x, pacman_y),
            (pacman_x + pacman_radius * pygame.math.Vector2(1, 0).rotate(30).x, 
             pacman_y + pacman_radius * pygame.math.Vector2(1, 0).rotate(30).y),
            (pacman_x + pacman_radius * pygame.math.Vector2(1, 0).rotate(-30).x, 
             pacman_y + pacman_radius * pygame.math.Vector2(1, 0).rotate(-30).y)
        ])
        screen.blit(welcome_text, welcome_rect)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    blink = True
    blink_start = time.time()

    while time.time() - blink_start < 3:
        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), pacman_radius)
        pygame.draw.polygon(screen, BLACK, [
            (pacman_x, pacman_y),
            (pacman_x + pacman_radius * pygame.math.Vector2(1, 0).rotate(30).x, 
             pacman_y + pacman_radius * pygame.math.Vector2(1, 0).rotate(30).y),
            (pacman_x + pacman_radius * pygame.math.Vector2(1, 0).rotate(-30).x, 
             pacman_y + pacman_radius * pygame.math.Vector2(1, 0).rotate(-30).y)
        ])
        screen.blit(welcome_text, welcome_rect)
        if blink:
            screen.blit(start_text, start_rect)
            screen.blit(quit_text, quit_rect)
        blink = not blink
        pygame.display.flip()
        pygame.time.delay(500)

    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

def wait_for_user_input():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def select_difficulty(screen):
    # Create background
    background = create_pixel_background(screen.get_width(), screen.get_height())
    
    # Create retro font
    try:
        retro_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 36)
        title_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 48)
    except:
        retro_font = pygame.font.SysFont('courier', 36, bold=True)
        title_font = pygame.font.SysFont('courier', 48, bold=True)

    title_text = title_font.render("SELECT DIFFICULTY", True, YELLOW)
    title_shadow = title_font.render("SELECT DIFFICULTY", True, (100, 100, 0))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 150))

    easy_text = retro_font.render("1. EASY", True, GREEN)
    medium_text = retro_font.render("2. MEDIUM", True, YELLOW)
    hard_text = retro_font.render("3. HARD", True, RED)

    easy_rect = easy_text.get_rect(center=(screen.get_width() // 2, 300))
    medium_rect = medium_text.get_rect(center=(screen.get_width() // 2, 370))
    hard_rect = hard_text.get_rect(center=(screen.get_width() // 2, 440))

    # Draw ghosts for decoration
    ghost_size = 40
    blinky_rect = pygame.Rect(150, 300, ghost_size, ghost_size)
    pinky_rect = pygame.Rect(150, 370, ghost_size, ghost_size)
    inky_rect = pygame.Rect(150, 440, ghost_size, ghost_size)
    
    clyde_rect = pygame.Rect(screen.get_width() - 200, 300, ghost_size, ghost_size)
    ghost2_rect = pygame.Rect(screen.get_width() - 200, 370, ghost_size, ghost_size)
    ghost3_rect = pygame.Rect(screen.get_width() - 200, 440, ghost_size, ghost_size)

    while True:
        screen.blit(background, (0, 0))
        
        # Draw title with shadow
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title_text, title_rect)
        
        # Draw options
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        
        # Draw ghosts
        pygame.draw.rect(screen, RED, blinky_rect, border_radius=20)
        pygame.draw.rect(screen, PINK, pinky_rect, border_radius=20)
        pygame.draw.rect(screen, BLUE, inky_rect, border_radius=20)
        
        pygame.draw.rect(screen, (255, 165, 0), clyde_rect, border_radius=20)  # Orange
        pygame.draw.rect(screen, GREEN, ghost2_rect, border_radius=20)
        pygame.draw.rect(screen, (128, 0, 128), ghost3_rect, border_radius=20)  # Purple
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Easy"
                elif event.key == pygame.K_2:
                    return "Medium"
                elif event.key == pygame.K_3:
                    return "Hard"

def display_game_manual(screen):
    """Display game instructions"""
    background = create_pixel_background(screen.get_width(), screen.get_height())
    
    try:
        retro_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 24)
        title_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'fonts/PressStart2P-Regular.ttf'), 36)
    except:
        retro_font = pygame.font.SysFont('courier', 24, bold=True)
        title_font = pygame.font.SysFont('courier', 36, bold=True)

    title = title_font.render("HOW TO PLAY", True, YELLOW)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 80))

    instructions = [
        "Use ARROW KEYS to move Pac-Man",
        "Eat all the dots to advance",
        "Avoid the ghosts!",
        "Power pellets let you eat ghosts",
        "Eat fruit for bonus points",
        "",
        "Difficulty affects ghost speed",
        "and point values",
        "",
        "Press ENTER to begin!"
    ]

    while True:
        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)

        y_offset = 150
        for line in instructions:
            text = retro_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def main():
    # Set up the display
    screen_width, screen_height = 800, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pac-Man")

    # Main game loop
    font = pygame.font.Font(None, 36)
    
    # Get player name
    player_name = get_player_name(screen, font)
    
    # Display welcome message
    display_welcome_message(screen, font, player_name)
    
    # Wait for user to press enter
    wait_for_user_input()
    
    # Show game manual
    display_game_manual(screen)
    
    # Select difficulty
    difficulty = select_difficulty(screen)
    
    # Here you would start the actual game with the selected difficulty
    print(f"Starting game for {player_name} at {difficulty} difficulty")
    
    # Game would continue here...
    # For now we'll just quit
    pygame.quit()

if __name__ == "__main__":
    main()