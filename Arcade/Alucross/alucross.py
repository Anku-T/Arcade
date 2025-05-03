import pygame
import math
import os
import time
import sys

pygame.init()

# Get screen size
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Screen
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TicTacToe")

# Determine the size of the Tic Tac Toe grid
GRID_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.8  # 80% of the smaller dimension
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_SIZE) // 2
ROWS = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
dir = os.path.dirname(os.path.abspath(__file__))

X_IMAGE = pygame.transform.scale(pygame.image.load(f"{dir}/files/x.png"), (GRID_SIZE // ROWS, GRID_SIZE // ROWS))
O_IMAGE = pygame.transform.scale(pygame.image.load(f"{dir}/files/o.png"), (GRID_SIZE // ROWS, GRID_SIZE // ROWS))
BACK_IMAGE = pygame.image.load(f"{dir}/files/back.png")
BACK_IMAGE = pygame.transform.scale(BACK_IMAGE, (50, 50))

# Fonts
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

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = GRID_OFFSET_X + dis_to_cen * (2 * j + 1)
            y = GRID_OFFSET_Y + dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array, back_button):
    global x_turn, o_turn, images, run

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    # Check if back button is clicked
    if back_button.is_clicked((m_x, m_y)):
        '''
        back button shit
        '''
        return

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < GRID_SIZE // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)

                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
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
    win.blit(end_text, ((SCREEN_WIDTH - end_text.get_width()) // 2, (SCREEN_HEIGHT - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render(back_button):
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    # Drawing the back button
    back_button.draw(win)

    pygame.display.update()


def main():
    global x_turn, o_turn, images, draw, run

    while True:
        images = []
        draw = False

        run = True

        x_turn = True
        o_turn = False

        game_array = initialize_grid()

        back_button = Button(BACK_IMAGE, SCREEN_WIDTH - 110, SCREEN_HEIGHT - 110, 100, 100)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click(game_array, back_button)

            render(back_button)

            if has_won(game_array) or has_drawn(game_array):
                run = False

if __name__ == '__main__':
    main()