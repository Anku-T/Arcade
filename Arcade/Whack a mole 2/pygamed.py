import pygame
import os
import random
import sys
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h
print(SCREEN_WIDTH, SCREEN_HEIGHT)
# Colors
AMAZON = (59, 122, 87)
BLUE_VIOLET = (138, 43, 226)
BLACK_OLIVE = (61, 61, 61)
ROSE_RED = (255, 0, 127)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
MENU = "menu"
PLAYING = "playing"
HOW_TO_PLAY = "how_to_play"
GAME_OVER = "game_over"

# Load assets
dir = os.path.dirname(os.path.abspath(__file__))
background_image = pygame.image.load(f"{dir}/files/home screen.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_button_image = pygame.image.load(f"{dir}/files/start_button.png")
start_button_image = pygame.transform.scale(start_button_image, (int(SCREEN_WIDTH * 0.18), int(SCREEN_HEIGHT * 0.13)))

htp_button_image = pygame.image.load(f"{dir}/files/htp_button.png")
htp_button_image = pygame.transform.scale(htp_button_image, (int(SCREEN_WIDTH * 0.18), int(SCREEN_HEIGHT * 0.13)))

how_to_play_image = pygame.image.load(f"{dir}/files/how.png")
how_to_play_image = pygame.transform.scale(how_to_play_image, (int(SCREEN_WIDTH*0.7), int(SCREEN_HEIGHT * 0.7)))

musa_image = pygame.image.load(f"{dir}/files/musa.png")
musa_image = pygame.transform.scale(musa_image, (int(musa_image.get_width()*SCREEN_WIDTH/1802), (int(musa_image.get_width()*SCREEN_WIDTH/1802))))

dead_musa_image = pygame.image.load(f"{dir}/files/dead musa.png")
dead_musa_image = pygame.transform.scale(dead_musa_image, (int(musa_image.get_width()*SCREEN_WIDTH/1802), (int(musa_image.get_width()*SCREEN_WIDTH/1802))))

shiny_musa_image = pygame.image.load(f"{dir}/files/shiny musa.png")
shiny_musa_image = pygame.transform.scale(shiny_musa_image, (int(musa_image.get_width()*SCREEN_WIDTH/1802), (int(musa_image.get_width()*SCREEN_WIDTH/1802))))

dead_shiny_musa_image = pygame.image.load(f"{dir}/files/dead shiny musa.png")
dead_shiny_musa_image = pygame.transform.scale(dead_shiny_musa_image, (int(musa_image.get_width()*SCREEN_WIDTH/1802), (int(musa_image.get_width()*SCREEN_WIDTH/1802))))

BACK_IMAGE = pygame.image.load(f"{dir}/files/back.png")
BACK_IMAGE = pygame.transform.scale(BACK_IMAGE,(int(musa_image.get_width() * 0.8), int(musa_image.get_height() * 0.8)))

# Load sounds
background_music = pygame.mixer.Sound(f"{dir}/files/background_music.mp3")
rat_sound = pygame.mixer.Sound(f"{dir}/files/rat_sound.mp3")
new_highscore_sound = pygame.mixer.Sound(f"{dir}/files/new_highscore.mp3")
victory_sound = pygame.mixer.Sound(f"{dir}/files/victoryy.mp3")

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack A Raticate™")


# Game variables
score = 0
highscore = 0
countdown = 76
game_state = MENU
rat_counter = 0
new_highscore = False
game_over_time = None

# Predefined positions for the rats
rat_positions = [
    (SCREEN_WIDTH / 4.5 , SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT/9)),
    (SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT/9)),
    (SCREEN_WIDTH / 1.3 , SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT/9)),
    (SCREEN_WIDTH / 2 -(SCREEN_WIDTH/6.5), SCREEN_HEIGHT / 2 + (SCREEN_HEIGHT/10)),
    (SCREEN_WIDTH / 2 +(SCREEN_WIDTH/8.5), SCREEN_HEIGHT / 2 + (SCREEN_HEIGHT/10)),
    (SCREEN_WIDTH / 4.5 , SCREEN_HEIGHT / 1.35),
    (SCREEN_WIDTH / 2.01 , SCREEN_HEIGHT / 1.35),
    (SCREEN_WIDTH / 1.31 , SCREEN_HEIGHT / 1.35)
]

# Sprites
class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

class Musa(pygame.sprite.Sprite):
    def __init__(self, image, x, y, is_shiny=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.is_shiny = is_shiny
        self.dead = False
        self.spawn_time = time.time()
        self.hit_time = None

    def hit(self):
        if not self.dead:
            self.dead = True
            self.hit_time = time.time()
            if self.is_shiny:
                self.image = dead_shiny_musa_image
                return 250
            else:
                self.image = dead_musa_image
                return 10
        return 0

start_button = Button(start_button_image, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
htp_button = Button(htp_button_image, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.7)
back_button = Button(BACK_IMAGE, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)
how_to_play_sprite = Button(how_to_play_image, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
shiny_musa_sprite = Button(shiny_musa_image, SCREEN_WIDTH / 2, SCREEN_HEIGHT // 2 + 100)

all_sprites = pygame.sprite.Group()
all_sprites.add(start_button)
all_sprites.add(htp_button)
all_sprites.add(back_button)

musa_sprites = pygame.sprite.Group()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def spawn_rat():
    global rat_counter
    if rat_counter < 76:
        x, y = random.choice(rat_positions)
        if rat_counter == 42:
            musa = Musa(shiny_musa_image, x, y, is_shiny=True)
        else:
            musa = Musa(musa_image, x, y)
        musa_sprites.add(musa)
        rat_counter += 1
        pygame.mixer.Sound.play(rat_sound)

def show_countdown():
    font = pygame.font.SysFont("Calibri", 74, bold=True)
    for i in range(3, 0, -1):
        screen.fill(AMAZON)
        text = font.render(str(i), True, BLUE_VIOLET)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1)
    screen.fill(AMAZON)
    text = font.render("Go!!", True, BLUE_VIOLET)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1)

def reset_game():
    global score, countdown, rat_counter, new_highscore
    score = 0
    countdown = 76
    rat_counter = 0
    new_highscore = False
    musa_sprites.empty()
    
    
def load_highscore(file_path):
    try:
        with open(file_path, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(file_path, highscore):
    with open(file_path, "w") as file:
        file.write(str(highscore))

def main():
    global score, highscore, countdown, game_state, new_highscore, game_over_time
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Calibri", 36, bold=True)

    highscore_file = os.path.join(dir, "highscore.txt")
    highscore = load_highscore(highscore_file)

    running = True

    while running:
        screen.fill(AMAZON)
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == MENU:
                    if start_button.rect.collidepoint(event.pos):
                        show_countdown()
                        game_state = PLAYING
                        pygame.mixer.Sound.play(background_music)
                        spawn_rat()  # Spawn the first rat after the countdown
                    elif htp_button.rect.collidepoint(event.pos):
                        game_state = HOW_TO_PLAY
                elif game_state == HOW_TO_PLAY:
                    game_state = MENU
                elif game_state == PLAYING:
                    for musa in musa_sprites:
                        if not musa.dead and musa.rect.collidepoint(event.pos):
                            score += musa.hit()
                            countdown -= 1
                elif game_state == GAME_OVER:
                    if time.time() - game_over_time > 2:
                        reset_game()
                        game_state = MENU

        if game_state == MENU:
            all_sprites.draw(screen)
        elif game_state == PLAYING:
            musa_sprites.draw(screen)

            # Remove rats if they are not hit within the time limit
            for musa in musa_sprites:
                if musa.dead and time.time() - musa.hit_time > 0.3:
                    musa_sprites.remove(musa)
                    spawn_rat()
                elif not musa.dead:
                    if musa.is_shiny and time.time() - musa.spawn_time > 0.5:
                        musa_sprites.remove(musa)
                        countdown -= 1
                        spawn_rat()
                    elif not musa.is_shiny and time.time() - musa.spawn_time > 0.7:
                        musa_sprites.remove(musa)
                        countdown -= 1
                        spawn_rat()

            # Check if the game should end
            if countdown <= 0:
                game_state = GAME_OVER
                game_over_time = time.time()
                pygame.mixer.Sound.stop(background_music)
                if score > highscore:
                    highscore = score
                    new_highscore = True
                    pygame.mixer.Sound.play(new_highscore_sound)
                elif score >= 1000:
                    highscore = score
                    new_highscore = True
                    pygame.mixer.Sound.play(victory_sound)

        elif game_state == HOW_TO_PLAY:
            screen.blit(how_to_play_image, how_to_play_sprite.rect)

        elif game_state == GAME_OVER:
            # Draw the black screen
            black_screen_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.draw.rect(screen, BLACK, black_screen_rect)

            # Draw the score and high score on the black screen
            draw_text(f"Score: {score}", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(f"High Score: {highscore}", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

            # Draw "New Highscore!!" if the score is a new high score
            if new_highscore:
                draw_text("New Highscore!!", font, ROSE_RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            elif score == 1000:
                draw_text("You win!!", font, ROSE_RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

            # Draw the shiny rat sprite at the center bottom of the black screen
            screen.blit(shiny_musa_image, (SCREEN_WIDTH // 2 - shiny_musa_image.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        # Draw the score and high score on the screen only if not in GAME_OVER state
        if game_state != GAME_OVER:
            draw_text(f"Score: {score}", font, BLUE_VIOLET, screen, SCREEN_WIDTH / 7, SCREEN_HEIGHT / 5)
            draw_text(f"High Score: {highscore}", font, ROSE_RED, screen, SCREEN_WIDTH / 1.2, SCREEN_HEIGHT / 5)

        # Draw the rats left counter only in the playing state
        if game_state == PLAYING:
            draw_text(f"Rats Left: {countdown}", font, BLACK_OLIVE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5)


        # Check if the back button is clicked
        # if back_button.rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            '''
            back button shit
            '''
            # return
        pygame.display.flip()
        clock.tick(60)

    # Save the high score before exiting
    save_highscore(highscore_file, highscore)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()