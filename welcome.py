import csv
import pygame
import time
import os

# Initialize pygame
pygame.init()

# Get the directory where the script is running
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
HIGHSCORE_PATH = os.path.join(SCRIPT_DIR, "highscore.csv")

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

def get_player_name(screen, font):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    input_text = ''
    active = True
    cursor_visible = True
    cursor_timer = 0

    high_scorer, high_score = load_high_score()
    all_scores = load_all_high_scores()

    while active:
        screen.fill(BLACK)

        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("PACMAN", True, YELLOW)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect)

        # High Score
        high_score_text = font.render(f"High Score: {high_score} by {high_scorer}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(screen.get_width() // 2, 180))
        screen.blit(high_score_text, high_score_rect)

        # Display top 5 ranks with improved UI
        ranks_box_width = 400
        ranks_box_height = 180
        ranks_box_x = (screen.get_width() - ranks_box_width) // 2
        ranks_box_y = 230
        ranks_box_rect = pygame.Rect(ranks_box_x, ranks_box_y, ranks_box_width, ranks_box_height)
        pygame.draw.rect(screen, (50, 50, 50), ranks_box_rect, border_radius=10)
        pygame.draw.rect(screen, YELLOW, ranks_box_rect, 2, border_radius=10)

        y_offset = ranks_box_y + 20
        rank = 1
        for name, sc in all_scores[:5]:
            rank_text = font.render(f'{rank}. {name} - {sc}', True, YELLOW)
            rank_rect = rank_text.get_rect(center=(screen.get_width() // 2, y_offset))
            screen.blit(rank_text, rank_rect)
            y_offset += 30
            rank += 1

        # Input box
        box_width = 500
        box_height = 60
        input_box_rect = pygame.Rect((screen.get_width() - box_width) // 2, 500, box_width, box_height)
        pygame.draw.rect(screen, WHITE, input_box_rect, border_radius=8)
        pygame.draw.rect(screen, YELLOW, input_box_rect, 3, border_radius=8)

        prompt = font.render("Enter your name:", True, WHITE)
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 440))
        screen.blit(prompt, prompt_rect)

        input_display = font.render(input_text + ("|" if cursor_visible else ""), True, BLACK)
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
                    input_text += event.unicode

def display_welcome_message(screen, font, player_name):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    text_color = WHITE

    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(WHITE)

    welcome_text = font.render(f"Welcome {player_name} to Pacman!", True, text_color)
    start_text = font.render("Press ENTER to Start or Q to Quit", True, text_color)

    welcome_rect = welcome_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    try:
        logo_image = pygame.image.load(os.path.join(SCRIPT_DIR, 'bg_images/bg.jpg'))
        logo_rect = logo_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    except pygame.error:
        logo_image = None
        print("Image could not be loaded. Please check the file path.")

    screen.fill(BLACK)

    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        if logo_image:
            screen.blit(logo_image, logo_rect)
        screen.blit(welcome_text, welcome_rect)
        pygame.display.flip()
        pygame.time.delay(30)

    blink = True
    blink_start = time.time()

    while time.time() - blink_start < 3:
        screen.fill(BLACK)
        if logo_image:
            screen.blit(logo_image, logo_rect)
        screen.blit(welcome_text, welcome_rect)
        if blink:
            screen.blit(start_text, start_rect)
        blink = not blink
        pygame.display.flip()
        pygame.time.delay(500)

    screen.blit(start_text, start_rect)
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

def select_difficulty(screen, font):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    title_font = pygame.font.Font(None, 60)
    title_text = title_font.render("Select Difficulty", True, YELLOW)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 200))

    easy_text = font.render("Press 1 for Easy", True, WHITE)
    medium_text = font.render("Press 2 for Medium", True, WHITE)
    hard_text = font.render("Press 3 for Hard", True, WHITE)

    easy_rect = easy_text.get_rect(center=(screen.get_width() // 2, 300))
    medium_rect = medium_text.get_rect(center=(screen.get_width() // 2, 360))
    hard_rect = hard_text.get_rect(center=(screen.get_width() // 2, 420))

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
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