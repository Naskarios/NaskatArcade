import pygame
import sys
import stuff


# https://github.com/Gooodgis/dont-touch-my-presents
# Initialize Pygame
pygame.init()
font = pygame.font.SysFont(None, 50)
selected_option = 0

# Set up the display

mainMenu = stuff.Menu(
    ["Play", "Games", "Settings", "Credits", "Quit"],
    stuff.WHITE,
    stuff.FUSCHIA,
    "966310-3268471822.jpg",
)
# Main loop
options = mainMenu.menu_options
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
                mainMenu.execute(selected_option)
    # Blit the background image onto the screen
    stuff.screen.blit(mainMenu.bg_image, (0, 0))
    # Render menu options
    mainMenu.renderOption(selected_option, font)
    # Update the display
    pygame.display.flip()
