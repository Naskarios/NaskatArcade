import pygame
import sys
import random
import pong
import math
# https://github.com/Gooodgis/dont-touch-my-presents


# CONSTANTS
width = 900
height = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 212)
# Fonts
font = pygame.font.SysFont(None, 50)
selected_option = 0


def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
    t = pygame.time.get_ticks() / 2 % time
    y = math.sin(t / speed) * how_far + overall_y
    return int(y)


class Menu:
    def __init__(self, menu_options, menu_color, menu_bgColor, bg_image):
        self.menu_options = menu_options
        self.menu_color = menu_color
        self.menu_bgColor = menu_bgColor
        self.bg_image = pygame.transform.scale(
            pygame.image.load(bg_image), (width, height)
        )

    def renderOption(self, selected_option):  # Render menu options
        for i, option in enumerate(self.menu_options):
            text = font.render(option, True, self.menu_color)
            text_rect = text.get_rect(center=(400, 200 + i * 100))
            screen.blit(text, text_rect)
        pygame.draw.rect(screen, PINK, (275, 175 + selected_option * 100, 250, 75), 2)

    def getOptions(self):
        return self.menu_options

    def draw(self):
        self.renderOption(self)


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ARCADE")


# Load the image


mainMenu = Menu(
    ["Play", "Games", "Credits", "Quit"],
    WHITE,
    WHITE,
    "dribbble_4x-2388550374.png",
)
options = mainMenu.menu_options
# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(options)
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(options)

            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                if options[selected_option].__eq__(options[0]):
                    print("TWRA PAIZOUME")
                    pong.main()
                elif options[selected_option].__eq__(options[1]):
                    print("posa game tlk?")
                elif options[selected_option].__eq__(options[2]):
                    print("This game was made by naskarios")
                elif options[selected_option].__eq__(options[3]):
                    pygame.quit()
                    sys.exit()

    # Blit the background image onto the screen
    screen.blit(mainMenu.bg_image, (0, 0))

    # Render menu options
    mainMenu.renderOption(selected_option)

    # Update the display
    pygame.display.flip()
