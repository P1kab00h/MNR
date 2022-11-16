import pygame
from figther import Fighter


# Initialization
pygame.init()

# Game window variable
win_x = 1000
win_y = 500
bgd_floor = 267
floor_height = 82
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

# Colors definition
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Fighters variables
kenji_attack1_size = 200
kenji_idle_size = 200
kenji_scale = 2
kenji_offset = [89, 53]
kenji_data = [kenji_attack1_size, kenji_idle_size, kenji_scale, kenji_offset]

samuraiMack_attack1_size = 200
samuraiMack_idle_size = 200
samuraiMack_scale = 2
samuraiMack_offset = [85, 47]
samuraiMack_data = [samuraiMack_attack1_size, samuraiMack_idle_size, samuraiMack_scale, samuraiMack_offset]


# Load image BackGround to the size of screen: Surface
background_img = pygame.image.load(
    'assets/images/background/background.png').convert_alpha()

# Load figthers sprite
# Kenji
kenji_idle_sprite = pygame.image.load('assets/images/Kenji/Idle.png').convert_alpha()
kenji_attack1_sprite = pygame.image.load('assets/images/Kenji/Attack1.png').convert_alpha()
# Samurai Mack
samuraiMack_idle_sprite = pygame.image.load('assets/images/samuraiMack/Idle.png').convert_alpha()
samuraiMack_attack1_sprite = pygame.image.load('assets/images/samuraiMack/Attack1.png').convert_alpha()

# Define number of sprite in an animation
kenji_idle_steps = 4
kenji_attack1_steps = 4


samuraiMack_idle_steps = 8
samuraiMack_attack1_steps = 6

# Draw background function,
# Scale the image on the 'screen' size
# origin => top left corner
def drw_bg():
    background_scale = pygame.transform.scale(background_img, (win_x, win_y))
    screen.blit(background_scale, (0, 0))

# Draw players life bars
def drw_life_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, white, (x - 3, y - 3, 406, 36))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, blue, (x, y, 400 * ratio, 30))
    


# Instances of Figther()
figther_1 = Fighter(200, bgd_floor, samuraiMack_data, samuraiMack_idle_sprite, samuraiMack_idle_steps)
#figther_1 = Fighter(200, bgd_floor)
figther_2 = Fighter(500, bgd_floor, kenji_data, kenji_idle_sprite, kenji_idle_steps)
#figther_2 = Fighter(500, bgd_floor)

# Game loop
run = True

while run:
    # handle the framerate
    clock.tick(fps)
    # Draw background
    drw_bg()
    # Draw Health Bars
    drw_life_bar(figther_1.health, 20, 20)
    drw_life_bar(figther_2.health, 580, 20)
    # manage figthers movement
    figther_1.move(win_x, win_y, floor_height, screen, figther_2)
    figther_2.move(win_x, win_y, floor_height, screen, figther_1)

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
