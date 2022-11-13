import pygame
from figther import Fighter


# Initialization
pygame.init()

# Game window variable
win_x = 1000
win_y = 500
# Screen size definition
screen = pygame.display.set_mode((win_x, win_y))

# Icon
icon = pygame.image.load('assets/images/icone/doomGuy.png')
# Set the icon
pygame.display.set_icon(icon)

# Title
pygame.display.set_caption('- Moon Nigth Rising -')

# Set the framerate
clock = pygame.time.Clock()
fps = 60

# Load image BackGround to the size of screen: Surface
background_img = pygame.image.load(
    'assets/images/background/background.png').convert_alpha()


# Draw background function,
# Scale the image on the 'screen' size
# origin => top left corner
def drw_bg():
    background_scale = pygame.transform.scale(background_img, (win_x, win_y))
    screen.blit(background_scale, (0, 0))


# Instances of Figther()
figther_1 = Fighter(200, 267)
figther_2 = Fighter(700, 267)


# Game loop
run = True

while run:
    # handle the framerate
    clock.tick(fps)
    # Draw background
    drw_bg()
    # manage figthers movement
    figther_1.move(win_x)
    figther_2.move(win_x)
    # Draw Figthers
    figther_1.drawFigther(screen)
    figther_2.drawFigther(screen)
    # Add Title
    sysFont = pygame.font.SysFont('arial', 42, True)
    rendered = sysFont.render('Moon Nigth Rising', 0, (255, 100, 100))
    screen.blit(rendered, (350, 425))

    # Event handler
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()
# Exit pygame
pygame.quit()
