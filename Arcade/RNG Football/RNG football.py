import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Get the screen size
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

dir = os.path.dirname(os.path.abspath(__file__))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RNG Football")

# Load background image
background_image = pygame.image.load(f"{dir}/files/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_button_image = pygame.image.load(f"{dir}/files/start_button.png")
start_button_image = pygame.transform.scale(start_button_image, (int(SCREEN_WIDTH * 0.18), int(SCREEN_HEIGHT * 0.13)))

striker_button_image = pygame.image.load(f"{dir}/files/striker_button.png")
striker_button_image = pygame.transform.scale(striker_button_image, (int(SCREEN_WIDTH * 0.18), int(SCREEN_HEIGHT * 0.13)))

keeper_button_image = pygame.image.load(f"{dir}/files/keeper_button.png")
keeper_button_image = pygame.transform.scale(keeper_button_image, (int(SCREEN_WIDTH * 0.18), int(SCREEN_HEIGHT * 0.13)))

htp_button_image = pygame.image.load(f"{dir}/files/htp_button.png")
htp_button_image = pygame.transform.scale(htp_button_image, (int(SCREEN_WIDTH * 0.18), int(SCREEN_HEIGHT * 0.13)))

how_to_play_image = pygame.image.load(f"{dir}/files/how.png")
how_to_play_image = pygame.transform.scale(how_to_play_image, (int(SCREEN_WIDTH*0.7), int(SCREEN_HEIGHT * 0.7)))

BACK_IMAGE = pygame.image.load(f"{dir}/files/back.png")
BACK_IMAGE = pygame.transform.scale(BACK_IMAGE, (int(204 * 0.8), int(204 * 0.8)))

# Load keeper and ball images
keeper_sprite_image = pygame.image.load(f"{dir}/files/keeper.png")
keeper_sprite_image = pygame.transform.scale(keeper_sprite_image, (int(keeper_sprite_image.get_width() * SCREEN_WIDTH/1440), int(keeper_sprite_image.get_height() * SCREEN_HEIGHT/900)))

ball_sprite_image = pygame.image.load(f"{dir}/files/ball.png")
ball_sprite_image = pygame.transform.scale(ball_sprite_image, (int(ball_sprite_image.get_width() * SCREEN_WIDTH/4868), int(ball_sprite_image.get_height() * SCREEN_HEIGHT/3000)))

# Load direction buttons
up_button_image = pygame.image.load(f"{dir}/files/up.png")
right_button_image = pygame.image.load(f"{dir}/files/right.png")
left_button_image = pygame.image.load(f"{dir}/files/left.png")

# Scale direction buttons to be a fraction bigger than the ball
button_scale_factor = 1
up_button_image = pygame.transform.scale(up_button_image, (int(ball_sprite_image.get_width() * button_scale_factor), int(ball_sprite_image.get_height() * button_scale_factor)))
right_button_image = pygame.transform.scale(right_button_image, (int(ball_sprite_image.get_width() * button_scale_factor), int(ball_sprite_image.get_height() * button_scale_factor)))
left_button_image = pygame.transform.scale(left_button_image, (int(ball_sprite_image.get_width() * button_scale_factor), int(ball_sprite_image.get_height() * button_scale_factor)))

# Load sounds
bg_music = pygame.mixer.Sound(f"{dir}/files/bg.wav")
save_sound = pygame.mixer.Sound(f"{dir}/files/save.wav")
score_sound = pygame.mixer.Sound(f"{dir}/files/score.wav")
shoot_sound = pygame.mixer.Sound(f"{dir}/files/shoot.wav")

# Define game modes
MAIN_MENU = "Main Menu"
PLAYING_SHOOTER = "Playing_Shooter"
PLAYING_KEEPER = "Playing_Keeper"
GAME_OVER = "Game Over"

# Set initial game mode
game_mode = MAIN_MENU

# Flag to show/hide how to play image
show_how_to_play = False

# Flag to show/hide keeper and ball sprites
show_keeper_and_ball = False

# Initialize score and kicks left
score = 0
kicks_left = 10

# Set up font
font = pygame.font.Font(None, 90)
flag_font = pygame.font.Font(None, 60)
game_over_font = pygame.font.Font(None, 72)

class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.enabled = True

    def draw(self, surface):
        if self.enabled:
            surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)

# Create buttons
start_button = Button(start_button_image, SCREEN_WIDTH // 2 - start_button_image.get_width() // 2, SCREEN_HEIGHT // 2 - start_button_image.get_height() // 2)
htp_button = Button(htp_button_image, SCREEN_WIDTH // 2 - htp_button_image.get_width() // 2, SCREEN_HEIGHT // 2 + start_button_image.get_height() // 2 + 20)
back_button = Button(BACK_IMAGE, SCREEN_WIDTH - BACK_IMAGE.get_width() - 20, SCREEN_HEIGHT - BACK_IMAGE.get_height() - 20)
striker_button = Button(striker_button_image, SCREEN_WIDTH // 2 - striker_button_image.get_width() - 10, SCREEN_HEIGHT // 2 - striker_button_image.get_height() // 2)
keeper_button = Button(keeper_button_image, SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - keeper_button_image.get_height() // 2)
up_button = Button(up_button_image, SCREEN_WIDTH // 2 - up_button_image.get_width() // 2, SCREEN_HEIGHT - ball_sprite_image.get_height() - 50)
right_button = Button(right_button_image, SCREEN_WIDTH // 2 + up_button_image.get_width() // 2 + 10, SCREEN_HEIGHT - ball_sprite_image.get_height() - 50)
left_button = Button(left_button_image, SCREEN_WIDTH // 2 - up_button_image.get_width() // 2 - left_button_image.get_width() - 10, SCREEN_HEIGHT - ball_sprite_image.get_height() - 50)

# Flag to indicate if a shot is in progress
shot_in_progress = False

# Flag to indicate if game over screen is active
game_over_active = False

def main_menu():
    screen.blit(background_image, (0, 0))  # Draw background image
    start_button.draw(screen)
    htp_button.draw(screen)
    back_button.draw(screen)
    if show_how_to_play:
        screen.blit(how_to_play_image, (SCREEN_WIDTH // 2 - how_to_play_image.get_width() // 2, SCREEN_HEIGHT // 2 - how_to_play_image.get_height() // 2))

def draw_labels():
    # Draw score and kicks left
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    kicks_left_text = font.render(f"Kicks left: {kicks_left}", True, (255, 255, 255))
    flag_color = (0, 255, 0) if not shot_in_progress else (255, 255, 255)
    shoot_text = flag_font.render("██", True, flag_color)
    score_bg = pygame.Surface(score_text.get_size())
    score_bg.fill((0, 100, 0))
    kicks_left_bg = pygame.Surface(kicks_left_text.get_size())
    kicks_left_bg.fill((0, 100, 0))
    shoot_bg = pygame.Surface(shoot_text.get_size())
    shoot_bg.fill((0, 0, 0))
    screen.blit(score_bg, (SCREEN_WIDTH - score_text.get_width() - 40, 40))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 40, 40))
    screen.blit(kicks_left_bg, (40, 40))
    screen.blit(kicks_left_text, (40, 40))
    screen.blit(shoot_bg, (SCREEN_WIDTH // 2 - shoot_text.get_width() // 2, 40))
    screen.blit(shoot_text, (SCREEN_WIDTH // 2 - shoot_text.get_width() // 2, 40))

    # Draw mode label
    if game_mode == PLAYING_SHOOTER:
        mode_text = font.render("Playing as Striker", True, (000, 000, 000))
        screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, SCREEN_HEIGHT - ball_sprite_image.get_height() -mode_text.get_height()*2.5))
    elif game_mode == PLAYING_KEEPER:
        mode_text = font.render("Playing as Keeper", True, (000, 000, 000))
        screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, SCREEN_HEIGHT - ball_sprite_image.get_height() -mode_text.get_height()*2.5))

def playing_shooter():
    screen.blit(background_image, (0, 0))  # Draw background image
    striker_button.draw(screen)
    keeper_button.draw(screen)
    if show_keeper_and_ball:
        screen.blit(keeper_sprite_image, (SCREEN_WIDTH // 2 - keeper_sprite_image.get_width() // 2, SCREEN_HEIGHT // 4 - keeper_sprite_image.get_height() // 2))
        screen.blit(ball_sprite_image, (SCREEN_WIDTH // 2 - ball_sprite_image.get_width() // 2, SCREEN_HEIGHT - ball_sprite_image.get_height() - 300))
        up_button.draw(screen)
        right_button.draw(screen)
        left_button.draw(screen)
    draw_labels()

def playing_keeper():
    screen.blit(background_image, (0, 0))  # Draw background image
    striker_button.draw(screen)
    keeper_button.draw(screen)
    if show_keeper_and_ball:
        screen.blit(keeper_sprite_image, (SCREEN_WIDTH // 2 - keeper_sprite_image.get_width() // 2, SCREEN_HEIGHT // 4 - keeper_sprite_image.get_height() // 2))
        screen.blit(ball_sprite_image, (SCREEN_WIDTH // 2 - ball_sprite_image.get_width() // 2, SCREEN_HEIGHT - ball_sprite_image.get_height() - 300))
        up_button.draw(screen)
        right_button.draw(screen)
        left_button.draw(screen)
    draw_labels()

def game_over():
    screen.blit(background_image, (0, 0))  # Draw background image
    back_button.draw(screen)
    # Add game over drawing and logic here
    game_over_bg = pygame.Surface((how_to_play_image.get_width(), how_to_play_image.get_height()))
    game_over_bg.fill((0, 0, 0))
    screen.blit(game_over_bg, (SCREEN_WIDTH // 2 - game_over_bg.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_bg.get_height() // 2))
    game_over_text = game_over_font.render("Game Over!!", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_bg.get_height() // 2 + 20))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2))
    if score < 200:
        remark_text = font.render("Luck Isn't with you", True, (255, 255, 255))
    elif score < 500:
        remark_text = font.render("You're quite lucky", True, (255, 255, 255))
    else:
        remark_text = font.render("You're Very lucky! You won!", True, (255, 255, 255))
    screen.blit(remark_text, (SCREEN_WIDTH // 2 - remark_text.get_width() // 2, SCREEN_HEIGHT // 2 + score_text.get_height()))

def animate_keeper_and_ball(keeper_x, keeper_y, ball_x, ball_y, direction, ball_position):
    global score, kicks_left, shot_in_progress, game_mode, game_over_active

    # Animate the keeper and ball simultaneously
    for i in range(15):
        screen.blit(background_image, (0, 0))
        if ball_position == 1:
            ball_x -= SCREEN_WIDTH/240
        elif ball_position == 3:
            ball_x += SCREEN_WIDTH/240
        ball_y -= SCREEN_HEIGHT/35
        if direction == "left":
            keeper_x -= SCREEN_WIDTH/240
        elif direction == "right":
            keeper_x += SCREEN_WIDTH/240
        screen.blit(keeper_sprite_image, (keeper_x, keeper_y))
        screen.blit(ball_sprite_image, (ball_x, ball_y - 20))  # Render the ball above the keeper
        draw_labels()
        pygame.display.flip()
        pygame.time.delay(10)

    # Check if the keeper catches the ball
    if (ball_position == 1 and direction == "left") or (ball_position == 2 and direction == "middle") or (ball_position == 3 and direction == "right"):
        # Keeper catches the ball
        save_sound.play()
        score += 50
    else:
        # Goal scored
        score_sound.play()

    # Update kicks left
    kicks_left -= 1

    # Reset shot in progress
    pygame.time.delay(1000)  # Add a 1-second wait time before the ball can be kicked again
    shot_in_progress = False
    up_button.enabled = True
    right_button.enabled = True
    left_button.enabled = True

    if kicks_left <= 0:
        game_mode = GAME_OVER
        game_over_active = True
        pygame.time.delay(2000)  # Freeze everything for 2 seconds

def move_keeper(direction):
    global shot_in_progress, score, kicks_left
    shot_in_progress = True
    up_button.enabled = False
    right_button.enabled = False
    left_button.enabled = False

    # Play shoot sound
    shoot_sound.play()

    # Move the keeper towards the ball
    keeper_x = SCREEN_WIDTH // 2 - keeper_sprite_image.get_width() // 2
    keeper_y = SCREEN_HEIGHT // 4 - keeper_sprite_image.get_height() // 2
    if direction == "left":
        keeper_x -= 100
    elif direction == "right":
        keeper_x += 100

    # Randomly determine the ball's position
    ball_position = random.randint(1, 3)
    ball_x = SCREEN_WIDTH // 2 - ball_sprite_image.get_width() // 2
    ball_y = SCREEN_HEIGHT - ball_sprite_image.get_height() - 300
    if ball_position == 1:
        ball_x -= 100
    elif ball_position == 3:
        ball_x += 100

    animate_keeper_and_ball(keeper_x, keeper_y, ball_x, ball_y, direction, ball_position)

def animate_ball_and_keeper(ball_x, ball_y, keeper_x, keeper_y, direction, keeper_position):
    global score, kicks_left, shot_in_progress, game_mode, game_over_active

    # Animate the ball and keeper simultaneously
    for i in range(15):
        screen.blit(background_image, (0, 0))
        if direction == "left":
            ball_x -= SCREEN_WIDTH/240
        elif direction == "right":
            ball_x += SCREEN_WIDTH/240
        ball_y -= SCREEN_HEIGHT/45
        if keeper_position == 1:
            keeper_x -= SCREEN_WIDTH/240
        elif keeper_position == 3:
            keeper_x += SCREEN_WIDTH/240
        screen.blit(keeper_sprite_image, (keeper_x, keeper_y))
        screen.blit(ball_sprite_image, (ball_x, ball_y - 20))  # Render the ball above the keeper
        draw_labels()
        pygame.display.flip()
        pygame.time.delay(10)

    # Check if the keeper catches the ball
    if (direction == "left" and keeper_position == 1) or (direction == "middle" and keeper_position == 2) or (direction == "right" and keeper_position == 3):
        # Keeper catches the ball
        save_sound.play()
    else:
        # Goal scored
        score += 50
        score_sound.play()

    # Update kicks left
    kicks_left -= 1

    # Reset shot in progress
    pygame.time.delay(1000)  # Add a 1-second wait time before the ball can be kicked again
    shot_in_progress = False
    up_button.enabled = True
    right_button.enabled = True
    left_button.enabled = True

    if kicks_left <= 0:
        game_mode = GAME_OVER
        game_over_active = True
        pygame.time.delay(2000)  # Freeze everything for 2 seconds

def shoot_ball(direction):
    global shot_in_progress, score, kicks_left
    shot_in_progress = True
    up_button.enabled = False
    right_button.enabled = False
    left_button.enabled = False

    # Play shoot sound
    shoot_sound.play()

    # Move the ball towards the goal
    ball_x = SCREEN_WIDTH // 2 - ball_sprite_image.get_width() // 2
    ball_y = SCREEN_HEIGHT - ball_sprite_image.get_height() - 300
    if direction == "left":
        ball_x -= 100
    elif direction == "right":
        ball_x += 100

    # Randomly determine the keeper's position
    keeper_position = random.randint(1, 3)
    keeper_x = SCREEN_WIDTH // 2 - keeper_sprite_image.get_width() // 2
    keeper_y = SCREEN_HEIGHT // 4 - keeper_sprite_image.get_height() // 2
    if keeper_position == 1:
        keeper_x -= 100
    elif keeper_position == 3:
        keeper_x += 100

    animate_ball_and_keeper(ball_x, ball_y, keeper_x, keeper_y, direction, keeper_position)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_mode = MAIN_MENU
                bg_music.stop()  # Stop background music
            elif event.key == pygame.K_2:
                game_mode = PLAYING_SHOOTER
                score = 0
                kicks_left = 10
                bg_music.play(-1)  # Play background music in loop
            elif event.key == pygame.K_3:
                game_mode = PLAYING_KEEPER
                score = 0
                kicks_left = 10
                bg_music.play(-1)  # Play background music in loop
            elif event.key == pygame.K_4:
                game_mode = GAME_OVER
                bg_music.stop()  # Stop background music
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == MAIN_MENU:
                if show_how_to_play:
                    show_how_to_play = False
                elif start_button.is_clicked(event.pos):
                    game_mode = PLAYING_SHOOTER
                    score = 0
                    kicks_left = 10
                    striker_button.enabled = True
                    keeper_button.enabled = True
                    bg_music.play(-1)  # Play background music in loop
                elif htp_button.is_clicked(event.pos):
                    show_how_to_play = True
                elif keeper_button.is_clicked(event.pos):
                    game_mode = PLAYING_KEEPER
                    score = 0
                    kicks_left = 10
                    striker_button.enabled = True
                    keeper_button.enabled = True
                    bg_music.play(-1)  # Play background music in loop
            elif game_mode == PLAYING_SHOOTER:
                if not shot_in_progress:
                    if up_button.is_clicked(event.pos):
                        shoot_ball("middle")
                    elif right_button.is_clicked(event.pos):
                        shoot_ball("right")
                    elif left_button.is_clicked(event.pos):
                        shoot_ball("left")
                if striker_button.is_clicked(event.pos):
                    show_keeper_and_ball = True
                    striker_button.enabled = False
                    keeper_button.enabled = False
                    game_mode = PLAYING_SHOOTER
                elif keeper_button.is_clicked(event.pos):
                    show_keeper_and_ball = True
                    striker_button.enabled = False
                    keeper_button.enabled = False
                    game_mode = PLAYING_KEEPER
            elif game_mode == PLAYING_KEEPER:
                if not shot_in_progress:
                    if up_button.is_clicked(event.pos):
                        move_keeper("middle")
                    elif right_button.is_clicked(event.pos):
                        move_keeper("right")
                    elif left_button.is_clicked(event.pos):
                        move_keeper("left")
            elif game_mode == GAME_OVER and not game_over_active:
                game_over_bg_rect = pygame.Rect(SCREEN_WIDTH // 2 - how_to_play_image.get_width() // 2, SCREEN_HEIGHT // 2 - how_to_play_image.get_height() // 2, how_to_play_image.get_width(), how_to_play_image.get_height())
                if not game_over_bg_rect.collidepoint(event.pos):
                    game_mode = MAIN_MENU
                    bg_music.stop()  # Stop background music

    # Update the display based on the game mode
    if game_mode == MAIN_MENU:
        main_menu()
    elif game_mode == PLAYING_SHOOTER:
        playing_shooter()
    elif game_mode == PLAYING_KEEPER:
        playing_keeper()
    elif game_mode == GAME_OVER:
        game_over()

    # Update the display
    pygame.display.flip()

    if game_mode == GAME_OVER and game_over_active:
        pygame.time.delay(2000)
        game_over_active = False

# Quit Pygame
pygame.quit()
sys.exit()