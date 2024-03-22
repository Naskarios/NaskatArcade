import pygame
import sys
import pong


# CONSTANTS-SETTINGS
WIDTH, HEIGHT = 900, 800
SNAKE_LOCK = 1
TETRIS_LOCK = 1
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 212)
FUSCHIA = (255, 77, 225)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ARCADE")
# INFO
gamesList = ["Pong", "Tetris", "Space Invaders", "Asteroids", "Snake", "2048?", "Quit"]
gamesLore = {
    "pong": [
        "Pong was the first game developed by Atari",
        'created by Allan Alcorn as a "a kind of warm-up exercise"',
        'Pong was "low-budget to the point of being a one-man operation",',
        " said the New York Post, and Alcorn took two months to create it.",
        'Atari sold thousands of Pong consoles, "the success of pong" saw the company "scrambling to staff up"',
        ' In 1973 Atari hired Steve Jobs,he was "asking for a job".',
        '"The most boring video game of all time", said IEEE, but 50 years',
        " since its release, gamers are still drawn to its “nostalgia”.",
    ]
}

# print(gamesLore["pong"][0])


# def audioService(gameslist):
#     pass


def menuSelectEventLoop(menu, font, screen):
    loopFlag = 1
    selected_option = 0
    while loopFlag == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu.menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu.menu_options)
                elif event.key == pygame.K_q:
                    loopFlag = 0
                    return loopFlag
                elif event.key == pygame.K_RETURN:
                    menu.execute(selected_option)
                    if selected_option == len(menu.menu_options) - 1:
                        loopFlag = 0
                        return loopFlag
        screen.blit(menu.bg_image, (0, 0))
        menu.renderOption(selected_option, font)
        pygame.display.flip()


# def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
#     t = pygame.time.get_ticks() / 2 % time
#     y = math.sin(t / speed) * how_far + overall_y
#     return int(y)


class Menu:
    def __init__(self, menu_options, menu_color, menu_selColor, bg_image):
        self.menu_options = menu_options
        self.menu_color = menu_color
        self.menu_selColor = menu_selColor
        self.bg_image = pygame.transform.scale(
            pygame.image.load(bg_image), (WIDTH, HEIGHT)
        )

    def renderOption(self, selected_option, font):  # Render menu options
        for i, option in enumerate(self.menu_options):
            # setting up the text with the font
            text = font.render(option, True, self.menu_color, None)
            # getting the rect where the text will be placed?
            text_rect = text.get_rect(center=(400, 100 + i * 100))
            # text_rect = text.get_rect(center=(400, 200 + i * 100))

            # drawing the text
            screen.blit(text, text_rect)
        # drawing the rect
        pygame.draw.rect(
            screen, self.menu_selColor, (275, 75 + selected_option * 100, 250, 75), 2
        )
        # pygame.draw.rect(
        #     screen, self.menu_selColor, (275, 175 + selected_option * 100, 250, 75), 2
        # )

    def getOptions(self):
        return self.menu_options

    def draw(self):
        self.renderOption(self)

    def execute(self, selected_option):
        if selected_option == 0:
            games = GameMenu(gamesList, WHITE, CYAN, "dribbble_4x-2388550374.png")
            menuSelectEventLoop(games, pygame.font.SysFont(None, 50), screen)
        elif selected_option == 1:
            print(gamesList)
        elif selected_option == 2:
            print("implement settings menu")
        elif selected_option == 3:
            print("Made by Naskarios")
        elif selected_option == 4:
            pygame.quit()
            sys.exit()


class GameMenu(Menu):
    def __init__(self, menu_options, menu_color, menu_selColor, bg_image):
        self.menu_options = menu_options
        self.menu_color = menu_color
        self.menu_selColor = menu_selColor
        self.bg_image = pygame.transform.scale(
            pygame.image.load(bg_image), (WIDTH, HEIGHT)
        )

    def execute(self, selected_option):
        if selected_option == 0:
            print("PONG")
            pong.main()
        elif selected_option == 1:
            print("Tetris")
        elif selected_option == 2:
            print("Space Invaders")
        elif selected_option == 3:
            print("Asteroids")
        elif selected_option == 4:
            print("Snake")
        elif selected_option == 5:
            print("2048")
