import subprocess
import os
import pygame
import sys
import math
import time
import random

# Initialize Pygame
pygame.init()

# Get screen size
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h-(8/100*screen_info.current_h)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# Load images
dir = os.path.dirname(os.path.abspath(__file__))
main_background = pygame.image.load(f"{dir}/main_background.png")
main_background = pygame.transform.scale(main_background, (screen_width, screen_height))

alucross_button_image = pygame.image.load(f"{dir}/alucross_icon.png")
alucross_button_image = pygame.transform.scale(alucross_button_image, (screen_width // 4, screen_width // 4))

whack_a_raticate_button_image = pygame.image.load(f"{dir}/Whack_a_raticate_icon.png")
whack_a_raticate_button_image = pygame.transform.scale(whack_a_raticate_button_image, (screen_width // 4, screen_width // 4))

rng_football_button_image = pygame.image.load(f"{dir}/rngfootball_icon.png")
rng_football_button_image = pygame.transform.scale(rng_football_button_image, (screen_width // 4, screen_width // 4))

# Define button properties
button_width = screen_width // 4
button_height = screen_width // 4
button_font = pygame.font.Font(None, 74)

# Define button positions
button1_rect = pygame.Rect((screen_width // 2 - button_width // 2, screen_height // 1.2 - button_height), (button_width, button_height))
button2_rect = pygame.Rect((screen_width // 6 - button_width // 2, screen_height // 1.2 - button_height), (button_width, button_height))
button3_rect = pygame.Rect((screen_width // 1.2 - button_width // 2, screen_height // 1.2 - button_height), (button_width, button_height))  # New button position

# Function to run Alucross game
def run_alucross():
    def main():
        pygame.init()
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        win = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("TicTacToe")
        GRID_SIZE = min(screen_width, screen_height) * 0.8
        GRID_OFFSET_X = (screen_width - GRID_SIZE) // 2
        GRID_OFFSET_Y = (screen_height - GRID_SIZE) // 2
        ROWS = 3
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        dir = os.path.dirname(os.path.abspath(__file__))
        X_IMAGE = pygame.transform.scale(pygame.image.load(f"{dir}/Alucross/files/x.png"), (GRID_SIZE // ROWS, GRID_SIZE // ROWS))
        O_IMAGE = pygame.transform.scale(pygame.image.load(f"{dir}/Alucross/files/o.png"), (GRID_SIZE // ROWS, GRID_SIZE // ROWS))
        BACK_IMAGE = pygame.image.load(f"{dir}/Alucross/files/back.png")
        BACK_IMAGE = pygame.transform.scale(BACK_IMAGE, (50, 50))
        END_FONT = pygame.font.SysFont('arial', int(GRID_SIZE // 10))

        class Button:
            def __init__(self, image, x, y, width, height):
                self.image = pygame.transform.scale(image, (width, height))
                self.rect = self.image.get_rect(topleft=(x, y))

            def draw(self, surface):
                surface.blit(self.image, (self.rect.x, self.rect.y))

            def is_clicked(self, pos):
                return self.rect.collidepoint(pos)

        def draw_grid():
            gap = GRID_SIZE // ROWS
            for i in range(ROWS + 1):
                pygame.draw.line(win, GRAY, (GRID_OFFSET_X + i * gap, GRID_OFFSET_Y), (GRID_OFFSET_X + i * gap, GRID_OFFSET_Y + GRID_SIZE), 3)
                pygame.draw.line(win, GRAY, (GRID_OFFSET_X, GRID_OFFSET_Y + i * gap), (GRID_OFFSET_X + GRID_SIZE, GRID_OFFSET_Y + i * gap), 3)

        def initialize_grid():
            dis_to_cen = GRID_SIZE // ROWS // 2
            game_array = [[None, None, None], [None, None, None], [None, None, None]]
            for i in range(len(game_array)):
                for j in range(len(game_array[i])):
                    x = GRID_OFFSET_X + dis_to_cen * (2 * j + 1)
                    y = GRID_OFFSET_Y + dis_to_cen * (2 * i + 1)
                    game_array[i][j] = (x, y, "", True)
            return game_array

        def click(game_array, back_button):
            global x_turn, o_turn, images, run
            m_x, m_y = pygame.mouse.get_pos()
            if back_button.is_clicked((m_x, m_y)):
                return False
            for i in range(len(game_array)):
                for j in range(len(game_array[i])):
                    x, y, char, can_play = game_array[i][j]
                    dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                    if dis < GRID_SIZE // ROWS // 2 and can_play:
                        if x_turn:
                            images.append((x, y, X_IMAGE))
                            x_turn = False
                            o_turn = True
                            game_array[i][j] = (x, y, 'x', False)
                        elif o_turn:
                            images.append((x, y, O_IMAGE))
                            x_turn = True
                            o_turn = False
                            game_array[i][j] = (x, y, 'o', False)
            return True

        def has_won(game_array):
            for row in range(len(game_array)):
                if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
                    display_message(game_array[row][0][2].upper() + " has won!")
                    return True
            for col in range(len(game_array)):
                if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
                    display_message(game_array[0][col][2].upper() + " has won!")
                    return True
            if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
                display_message(game_array[0][0][2].upper() + " has won!")
                return True
            if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
                display_message(game_array[0][2][2].upper() + " has won!")
                return True
            return False

        def has_drawn(game_array):
            for i in range(len(game_array)):
                for j in range(len(game_array[i])):
                    if game_array[i][j][2] == "":
                        return False
            display_message("It's a draw!")
            return True

        def display_message(content):
            pygame.time.delay(500)
            win.fill(WHITE)
            end_text = END_FONT.render(content, 1, BLACK)
            win.blit(end_text, ((screen_width - end_text.get_width()) // 2, (screen_height - end_text.get_height()) // 2))
            pygame.display.update()
            pygame.time.delay(3000)

        def render(back_button):
            win.fill(WHITE)
            draw_grid()
            for image in images:
                x, y, IMAGE = image
                win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))
            back_button.draw(win)
            pygame.display.update()

        global x_turn, o_turn, images, draw, run
        while True:
            images = []
            draw = False
            run = True
            x_turn = True
            o_turn = False
            game_array = initialize_grid()
            back_button = Button(BACK_IMAGE, screen_width - 110, screen_height - 110, 100, 100)
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not click(game_array, back_button):
                            return
                render(back_button)
                if has_won(game_array) or has_drawn(game_array):
                    run = False

    main()

# Function to run Whack A Raticate game
def run_whack_a_raticate():
    import random
    dir = os.path.dirname(os.path.abspath(__file__))

    def main():
        pygame.init()
        pygame.mixer.init()
        SCREEN_INFO = pygame.display.Info()
        screen_width = SCREEN_INFO.current_w
        screen_height = SCREEN_INFO.current_h
        AMAZON = (59, 122, 87)
        BLUE_VIOLET = (138, 43, 226)
        BLACK_OLIVE = (61, 61, 61)
        ROSE_RED = (255, 0, 127)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        MENU = "menu"
        PLAYING = "playing"
        HOW_TO_PLAY = "how_to_play"
        GAME_OVER = "game_over"
        dir = os.path.dirname(os.path.abspath(__file__))
        background_image = pygame.image.load(f"{dir}/Whack a mole 2/files/home screen.png")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        
        start_button_image = pygame.image.load(f"{dir}/Whack a mole 2/files/start_button.png")
        start_button_image = pygame.transform.scale(start_button_image, (int(screen_width * 0.18), int(screen_height * 0.13)))

        htp_button_image = pygame.image.load(f"{dir}/Whack a mole 2/files/htp_button.png")
        htp_button_image = pygame.transform.scale(htp_button_image, (int(screen_width * 0.18), int(screen_height * 0.13)))

        how_to_play_image = pygame.image.load(f"{dir}/Whack a mole 2/files/how.png")
        how_to_play_image = pygame.transform.scale(how_to_play_image, (int(screen_width*0.7), int(screen_height * 0.7)))

        musa_image = pygame.image.load(f"{dir}/Whack a mole 2/files/musa.png")
        musa_image = pygame.transform.scale(musa_image, (int(musa_image.get_width()*screen_width/1802), (int(musa_image.get_width()*screen_width/1802))))

        dead_musa_image = pygame.image.load(f"{dir}/Whack a mole 2/files/dead musa.png")
        dead_musa_image = pygame.transform.scale(dead_musa_image, (int(musa_image.get_width()*screen_width/1802), (int(musa_image.get_width()*screen_width/1802))))

        shiny_musa_image = pygame.image.load(f"{dir}/Whack a mole 2/files/shiny musa.png")
        shiny_musa_image = pygame.transform.scale(shiny_musa_image, (int(musa_image.get_width()*screen_width/1802), (int(musa_image.get_width()*screen_width/1802))))

        dead_shiny_musa_image = pygame.image.load(f"{dir}/Whack a mole 2/files/dead shiny musa.png")
        dead_shiny_musa_image = pygame.transform.scale(dead_shiny_musa_image, (int(musa_image.get_width()*screen_width/1802), (int(musa_image.get_width()*screen_width/1802))))


        BACK_IMAGE = pygame.image.load(f"{dir}/Whack a mole 2/files/back.png")
        BACK_IMAGE = pygame.transform.scale(BACK_IMAGE, (int(musa_image.get_width() * 0.8), int(musa_image.get_height() * 0.8)))
        
        background_music = pygame.mixer.Sound(f"{dir}/Whack a mole 2/files/background_music.mp3")
        
        rat_sound = pygame.mixer.Sound(f"{dir}/Whack a mole 2/files/rat_sound.mp3")
        
        new_highscore_sound = pygame.mixer.Sound(f"{dir}/Whack a mole 2/files/new_highscore.mp3")
        
        victory_sound = pygame.mixer.Sound(f"{dir}/Whack a mole 2/files/victoryy.mp3")
        
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        pygame.display.set_caption("Whack A Raticate™")

        global score, highscore, countdown, game_state, new_highscore, game_over_time, rat_counter

        score = 0
        highscore = 0
        countdown = 76
        game_state = MENU
        rat_counter = 0
        new_highscore = False
        game_over_time = None

        rat_positions = [
            (screen_width / 4.5 , screen_height / 3 + (screen_height/9)),
            (screen_width / 2 , screen_height / 3 + (screen_height/9)),
            (screen_width / 1.3 , screen_height / 3 + (screen_height/9)),
            (screen_width / 2 -(screen_width/6.5), screen_height / 2 + (screen_height/10)),
            (screen_width / 2 +(screen_width/8.5), screen_height / 2 + (screen_height/10)),
            (screen_width / 4.5 , screen_height / 1.35),
            (screen_width / 2.01 , screen_height / 1.35),
            (screen_width / 1.31 , screen_height / 1.35)
        ]

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

        start_button = Button(start_button_image, screen_width / 2, screen_height / 2)
        htp_button = Button(htp_button_image, screen_width / 2, screen_height / 1.7)
        back_button = Button(BACK_IMAGE, screen_width - 50, screen_height - 50)
        how_to_play_sprite = Button(how_to_play_image, screen_width / 2, screen_height / 2)
        shiny_musa_sprite = Button(shiny_musa_image, screen_width / 2, screen_height // 2 + 100)
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
                text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                time.sleep(1)
            screen.fill(AMAZON)
            text = font.render("Go!!", True, BLUE_VIOLET)
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
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
                black_screen_rect = pygame.Rect(screen_width // 4, screen_height // 3, screen_width // 2, screen_height // 2)
                pygame.draw.rect(screen, BLACK, black_screen_rect)

                # Draw the score and high score on the black screen
                draw_text(f"Score: {score}", font, WHITE, screen, screen_width // 2, screen_height // 2 - 50)
                draw_text(f"High Score: {highscore}", font, WHITE, screen, screen_width // 2, screen_height // 2 + 50)

                # Draw "New Highscore!!" if the score is a new high score
                if new_highscore:
                    draw_text("New Highscore!!", font, ROSE_RED, screen, screen_width // 2, screen_height // 2 - 100)
                elif score == 1000:
                    draw_text("You win!!", font, ROSE_RED, screen, screen_width // 2, screen_height // 2 - 100)

                # Draw the shiny rat sprite at the center bottom of the black screen
                screen.blit(shiny_musa_image, (screen_width // 2 - shiny_musa_image.get_width() // 2, screen_height // 2 + 100))

            # Draw the score and high score on the screen only if not in GAME_OVER state
            if game_state != GAME_OVER:
                draw_text(f"Score: {score}", font, BLUE_VIOLET, screen, screen_width / 7, screen_height / 5)
                draw_text(f"High Score: {highscore}", font, ROSE_RED, screen, screen_width / 1.2, screen_height / 5)

            # Draw the rats left counter only in the playing state
            if game_state == PLAYING:
                draw_text(f"Rats Left: {countdown}", font, BLACK_OLIVE, screen, screen_width / 2, screen_height / 5)

            # Check if the back button is clicked
            if game_state != PLAYING:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if back_button.rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    return

            pygame.display.flip()
            clock.tick(60)

        # Save the high score before exiting
        save_highscore(highscore_file, highscore)

        pygame.quit()
        sys.exit()

    main()

MAIN_MENU = "Main Menu"
PLAYING_SHOOTER = "Playing_Shooter"
PLAYING_KEEPER = "Playing_Keeper"
GAME_OVER = "Game Over"

# Function to run RNG Football game
def run_rng_football():
    global score, kicks_left, game_mode, show_how_to_play, show_keeper_and_ball, shot_in_progress, game_over_active
    global MAIN_MENU, PLAYING_SHOOTER, PLAYING_KEEPER, GAME_OVER
    
    dir = os.path.dirname(os.path.abspath(__file__))
    pygame.display.set_caption("RNG Football")
    # Load background image
    background_image = pygame.image.load(f"{dir}/RNG Football/files/background.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    start_button_image = pygame.image.load(f"{dir}/RNG Football/files/start_button.png")
    start_button_image = pygame.transform.scale(start_button_image, (int(screen_width * 0.18), int(screen_height * 0.13)))

    striker_button_image = pygame.image.load(f"{dir}/RNG Football/files/striker_button.png")
    striker_button_image = pygame.transform.scale(striker_button_image, (int(screen_width * 0.18), int(screen_height * 0.13)))

    keeper_button_image = pygame.image.load(f"{dir}/RNG Football/files/keeper_button.png")
    keeper_button_image = pygame.transform.scale(keeper_button_image, (int(screen_width * 0.18), int(screen_height * 0.13)))

    htp_button_image = pygame.image.load(f"{dir}/RNG Football/files/htp_button.png")
    htp_button_image = pygame.transform.scale(htp_button_image, (int(screen_width * 0.18), int(screen_height * 0.13)))

    how_to_play_image = pygame.image.load(f"{dir}/RNG Football/files/how.png")
    how_to_play_image = pygame.transform.scale(how_to_play_image, (int(screen_width*0.7), int(screen_height * 0.7)))

    BACK_IMAGE = pygame.image.load(f"{dir}/RNG Football/files/back.png")
    BACK_IMAGE = pygame.transform.scale(BACK_IMAGE, (int(204 * 0.8), int(204 * 0.8)))

    # Load keeper and ball images
    keeper_sprite_image = pygame.image.load(f"{dir}/RNG Football/files/keeper.png")
    keeper_sprite_image = pygame.transform.scale(keeper_sprite_image, (int(keeper_sprite_image.get_width() * screen_width/1440), int(keeper_sprite_image.get_height() * screen_height/900)))

    ball_sprite_image = pygame.image.load(f"{dir}/RNG Football/files/ball.png")
    ball_sprite_image = pygame.transform.scale(ball_sprite_image, (int(ball_sprite_image.get_width() * screen_width/4868), int(ball_sprite_image.get_height() * screen_height/3000)))

    # Load direction buttons
    up_button_image = pygame.image.load(f"{dir}/RNG Football/files/up.png")
    right_button_image = pygame.image.load(f"{dir}/RNG Football/files/right.png")
    left_button_image = pygame.image.load(f"{dir}/RNG Football/files/left.png")

    # Scale direction buttons to be a fraction bigger than the ball
    button_scale_factor = 1
    up_button_image = pygame.transform.scale(up_button_image, (int(ball_sprite_image.get_width() * button_scale_factor), int(ball_sprite_image.get_height() * button_scale_factor)))
    right_button_image = pygame.transform.scale(right_button_image, (int(ball_sprite_image.get_width() * button_scale_factor), int(ball_sprite_image.get_height() * button_scale_factor)))
    left_button_image = pygame.transform.scale(left_button_image, (int(ball_sprite_image.get_width() * button_scale_factor), int(ball_sprite_image.get_height() * button_scale_factor)))

    # Load sounds
    bg_music = pygame.mixer.Sound(f"{dir}/RNG Football/files/bg.wav")
    save_sound = pygame.mixer.Sound(f"{dir}/RNG Football/files/save.wav")
    score_sound = pygame.mixer.Sound(f"{dir}/RNG Football/files/score.wav")
    shoot_sound = pygame.mixer.Sound(f"{dir}/RNG Football/files/shoot.wav")
    victory_sound = pygame.mixer.Sound(f"{dir}/RNG Football/files/victory.mp3")

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
    start_button = Button(start_button_image, screen_width // 2 - start_button_image.get_width() // 2, screen_height // 2 - start_button_image.get_height() // 2)
    htp_button = Button(htp_button_image, screen_width // 2 - htp_button_image.get_width() // 2, screen_height // 2 + start_button_image.get_height() // 2 + 20)
    back_button = Button(BACK_IMAGE, screen_width - BACK_IMAGE.get_width() - 20, screen_height - BACK_IMAGE.get_height() - 20)
    striker_button = Button(striker_button_image, screen_width // 2 - striker_button_image.get_width() - 10, screen_height // 2 - striker_button_image.get_height() // 2)
    keeper_button = Button(keeper_button_image, screen_width // 2 + 10, screen_height // 2 - keeper_button_image.get_height() // 2)
    up_button = Button(up_button_image, screen_width // 2 - up_button_image.get_width() // 2, screen_height - ball_sprite_image.get_height() - 50)
    right_button = Button(right_button_image, screen_width // 2 + up_button_image.get_width() // 2 + 10, screen_height - ball_sprite_image.get_height() - 50)
    left_button = Button(left_button_image, screen_width // 2 - up_button_image.get_width() // 2 - left_button_image.get_width() - 10, screen_height - ball_sprite_image.get_height() - 50)

    # Flag to indicate if a shot is in progress
    shot_in_progress = False

    # Flag to indicate if game over screen is active
    game_over_active = False

    def main_menu():
        victory_sound.stop()
        screen.blit(background_image, (0, 0))  # Draw background image
        start_button.draw(screen)
        htp_button.draw(screen)
        back_button.draw(screen)
        if show_how_to_play:
            screen.blit(how_to_play_image, (screen_width // 2 - how_to_play_image.get_width() // 2, screen_height // 2 - how_to_play_image.get_height() // 2))

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
        screen.blit(score_bg, (screen_width - score_text.get_width() - 40, 40))
        screen.blit(score_text, (screen_width - score_text.get_width() - 40, 40))
        screen.blit(kicks_left_bg, (40, 40))
        screen.blit(kicks_left_text, (40, 40))
        screen.blit(shoot_bg, (screen_width // 2 - shoot_text.get_width() // 2, 40))
        screen.blit(shoot_text, (screen_width // 2 - shoot_text.get_width() // 2, 40))

        # Draw mode label
        if game_mode == PLAYING_SHOOTER:
            mode_text = font.render("Playing as Striker", True, (0, 0, 0))
            screen.blit(mode_text, (screen_width // 2 - mode_text.get_width() // 2, screen_height - ball_sprite_image.get_height() - mode_text.get_height() * 2.5))
        elif game_mode == PLAYING_KEEPER:
            mode_text = font.render("Playing as Keeper", True, (0, 0, 0))
            screen.blit(mode_text, (screen_width // 2 - mode_text.get_width() // 2, screen_height - ball_sprite_image.get_height() - mode_text.get_height() * 2.5))

    def playing_shooter():
        screen.blit(background_image, (0, 0))  # Draw background image
        striker_button.draw(screen)
        keeper_button.draw(screen)
        if show_keeper_and_ball:
            screen.blit(keeper_sprite_image, (screen_width // 2 - keeper_sprite_image.get_width() // 2, screen_height // 4 - keeper_sprite_image.get_height() // 2))
            screen.blit(ball_sprite_image, (screen_width // 2 - ball_sprite_image.get_width() // 2, screen_height - ball_sprite_image.get_height() - 300))
            up_button.draw(screen)
            right_button.draw(screen)
            left_button.draw(screen)
        draw_labels()

    def playing_keeper():
        screen.blit(background_image, (0, 0))  # Draw background image
        striker_button.draw(screen)
        keeper_button.draw(screen)
        if show_keeper_and_ball:
            screen.blit(keeper_sprite_image, (screen_width // 2 - keeper_sprite_image.get_width() // 2, screen_height // 4 - keeper_sprite_image.get_height() // 2))
            screen.blit(ball_sprite_image, (screen_width // 2 - ball_sprite_image.get_width() // 2, screen_height - ball_sprite_image.get_height() - 300))
            up_button.draw(screen)
            right_button.draw(screen)
            left_button.draw(screen)
        draw_labels()

    def game_over():
        global game_over_active

        screen.blit(background_image, (0, 0))  # Draw background image
        back_button.draw(screen)
        # Add game over drawing and logic here
        game_over_bg = pygame.Surface((how_to_play_image.get_width(), how_to_play_image.get_height()))
        game_over_bg.fill((0, 0, 0))
        screen.blit(game_over_bg, (screen_width // 2 - game_over_bg.get_width() // 2, screen_height // 2 - game_over_bg.get_height() // 2))
        game_over_text = game_over_font.render("Game Over!!", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_bg.get_height() // 2 + 20))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height() // 2))
        if score < 200:
            remark_text = font.render("Luck Isn't with you", True, (255, 255, 255))
        elif score < 500 and score >= 200:
            remark_text = font.render("You're quite lucky", True, (255, 255, 255))
        elif score >= 500:
            remark_text = font.render("You're Very lucky! You won!", True, (255, 255, 255))
            if not game_over_active:
                victory_sound.play()  
                pygame.time.delay(12000)
                game_over_active = True  
        screen.blit(remark_text, (screen_width // 2 - remark_text.get_width() // 2, screen_height // 2 + score_text.get_height()))
        bg_music.stop()


    def animate_keeper_and_ball(keeper_x, keeper_y, ball_x, ball_y, direction, ball_position):
        global score, kicks_left, shot_in_progress, game_mode, game_over_active

        # Animate the keeper and ball simultaneously
        for i in range(15):
            screen.blit(background_image, (0, 0))
            if ball_position == 1:
                ball_x -= screen_width/240
            elif ball_position == 3:
                ball_x += screen_width/240
            ball_y -= screen_height/45
            if direction == "left":
                keeper_x -= screen_width/240
            elif direction == "right":
                keeper_x += screen_width/240
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
        keeper_x = screen_width // 2 - keeper_sprite_image.get_width() // 2
        keeper_y = screen_height // 4 - keeper_sprite_image.get_height() // 2
        if direction == "left":
            keeper_x -= 100
        elif direction == "right":
            keeper_x += 100

        # Randomly determine the ball's position
        ball_position = random.randint(1, 3)
        ball_x = screen_width // 2 - ball_sprite_image.get_width() // 2
        ball_y = screen_height - ball_sprite_image.get_height() - 300
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
                ball_x -= screen_width/240
            elif direction == "right":
                ball_x += screen_width/240
            ball_y -= screen_height/45
            if keeper_position == 1:
                keeper_x -= screen_width/240
            elif keeper_position == 3:
                keeper_x += screen_width/240
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

        # Move the ball towards the keeper
        ball_x = screen_width // 2 - ball_sprite_image.get_width() // 2
        ball_y = screen_height - ball_sprite_image.get_height() - 300
        if direction == "left":
            ball_x -= 100
        elif direction == "right":
            ball_x += 100

        # Randomly determine the keeper's position
        keeper_position = random.randint(1, 3)
        keeper_x = screen_width // 2 - keeper_sprite_image.get_width() // 2
        keeper_y = screen_height // 4 - keeper_sprite_image.get_height() // 2
        if keeper_position == 1:
            keeper_x -= 100
        elif keeper_position == 3:
            keeper_x += 100

        animate_ball_and_keeper(ball_x, ball_y, keeper_x, keeper_y, direction, keeper_position)

    def main():
        global game_mode, show_how_to_play, show_keeper_and_ball, shot_in_progress, game_over_active, score, kicks_left

        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("RNG Football")

        clock = pygame.time.Clock()
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
                        game_over_bg_rect = pygame.Rect(screen_width // 2 - how_to_play_image.get_width() // 2, screen_height // 2 - how_to_play_image.get_height() // 2, how_to_play_image.get_width(), how_to_play_image.get_height())
                        if not game_over_bg_rect.collidepoint(event.pos):
                            game_mode = MAIN_MENU
                            bg_music.stop()  # Stop background music
                    # Check if the back button is clicked
                    if back_button.is_clicked(event.pos):
                        return

            # Update the display based on the game mode
            if game_mode == MAIN_MENU:
                main_menu()
            elif game_mode == PLAYING_SHOOTER:
                playing_shooter()
            elif game_mode == PLAYING_KEEPER:
                playing_keeper()
            elif game_mode == GAME_OVER:
                game_over()

            pygame.display.flip()

            if game_mode == GAME_OVER and game_over_active:
                pygame.time.delay(2000)
                game_over_active = False
                victory_sound.stop()

        pygame.quit()
        return

    main()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1_rect.collidepoint(event.pos):
                run_alucross()
            elif button2_rect.collidepoint(event.pos):
                run_whack_a_raticate()
            elif button3_rect.collidepoint(event.pos):
                run_rng_football()

    # Clear the screen and draw the background
    screen.blit(main_background, (0, 0))

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    if button1_rect.collidepoint(mouse_pos):
        screen.blit(alucross_button_image, button1_rect.topleft)
    else:
         screen.blit(alucross_button_image, button1_rect.topleft)
    if button2_rect.collidepoint(mouse_pos):
        screen.blit(whack_a_raticate_button_image, button2_rect.topleft)
    else:
        screen.blit(whack_a_raticate_button_image, button2_rect.topleft)
    if button3_rect.collidepoint(mouse_pos):
        screen.blit(rng_football_button_image, button3_rect.topleft)
    else:
        screen.blit(rng_football_button_image, button3_rect.topleft)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
