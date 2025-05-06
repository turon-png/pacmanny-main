import pygame
import time

def get_player_name(screen, font):
    """Let the user enter their name using keyboard input with styled UI."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    input_text = ''
    active = True
    cursor_visible = True
    cursor_timer = 0

    while active:
        screen.fill(BLACK)

        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("PACMAN", True, YELLOW)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        # Input box
        box_width = 500
        box_height = 60
        input_box_rect = pygame.Rect((screen.get_width() - box_width) // 2, 300, box_width, box_height)
        pygame.draw.rect(screen, WHITE, input_box_rect, border_radius=8)
        pygame.draw.rect(screen, YELLOW, input_box_rect, 3, border_radius=8)

        prompt = font.render("Enter your name:", True, WHITE)
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 260))
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
                    return input_text.strip() if input_text.strip() else "Player"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode


def display_welcome_message(screen, font, player_name):
    """Display welcome screen with fade-in and blinking start prompt."""
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
        logo_image = pygame.image.load('bg_images/bg.jpg')
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
    """Wait for the user to press Enter to start or Q to quit."""
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
    """Display difficulty selection screen and return choice."""
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
