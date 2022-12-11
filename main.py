import pygame
from pygame import mixer # will handle sound effect & music
from figther import Fighter


# Initialization
mixer.init()
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

# Game variables
start_countdown = 0 #3
last_countdown_update = pygame.time.get_ticks()

# Fighters variables
kenji_size = 200
kenji_scale = 2
kenji_offset = [89, 53]
kenji_data = [kenji_size, kenji_scale, kenji_offset]

samuraiMack_size = 200
samuraiMack_scale = 2
samuraiMack_offset = [85, 47]
samuraiMack_data = [samuraiMack_size, samuraiMack_scale, samuraiMack_offset]

# Load and play sound effects and musics
pygame.mixer.music.load("assets/sounds/currentUsed/DavidKBD-HairAndKnucklesPack-05-ANewAwakening.ogg")
pygame.mixer.music.set_volume(0.25) # handle the music volume
pygame.mixer.music.play(-1, 0.0, 5000) # allow to loop thrue the music (repeat -1, start at 0.0, and some fading)

sword_soundEffect = pygame.mixer.Sound("assets/sounds/currentUsed/RetroSwooosh16.wav")
sword_soundEffect.set_volume(1.1)

hit_soundEffect = pygame.mixer.Sound("assets/sounds/currentUsed/RetroImpactHurt.wav")

# volume to 0, searching for the good sound
jump_soundEffect = pygame.mixer.Sound("assets/sounds/currentUsed/RetroJumpStereoUPSimple05.wav")
#jump_soundEffect.set_volume(0)

# volume to 0, seraching for a good sound
walk_soundEffect = pygame.mixer.Sound("assets/sounds/currentUsed/walkMedium.wav")
#walk_soundEffect.set_volume(0)



# Load image BackGround to the size of screen: Surface
background_img = pygame.image.load(
    'assets/images/background/background.png').convert_alpha()

################### Load figthers sprite
#### Kenji
kenji_full_sprite = pygame.image.load('assets/images/Kenji/kenji-full-sprites.png').convert_alpha()
#kenji_idle_sprite = pygame.image.load('assets/images/Kenji/Idle.png').convert_alpha()
#kenji_attack1_sprite = pygame.image.load('assets/images/Kenji/Attack1.png').convert_alpha()
#kenji_run_sprite = pygame.image.load('assets/images/Kenji/Run.png').convert_alpha()
##### Samurai Mack
samuraiMack_full_sprite = pygame.image.load('assets/images/samuraiMack/samuraiMack-full-sprites.png').convert_alpha()
#samuraiMack_idle_sprite = pygame.image.load('assets/images/samuraiMack/Idle.png').convert_alpha()
#samuraiMack_attack1_sprite = pygame.image.load('assets/images/samuraiMack/Attack1.png').convert_alpha()
#samuraiMack_run_sprite = pygame.image.load('assets/images/samuraiMack/Run.png').convert_alpha()

##### Define number of sprite in an animation
# atck1, atck2, death, idle, jump, run, take hit
kenji_full_sprites_steps = [4, 4, 8, 4, 2, 8, 3]
#kenji_idle_steps = 4
#kenji_attack1_steps = 4
#kenji_run_steps = 8
samuraiMack_full_sprites_steps = [6, 6, 6, 8, 2, 8, 4]
#samuraiMack_idle_steps = 8
#samuraiMack_attack1_steps = 6
#samuraiMack_run_steps = 8

#Define fount
countdown_font = pygame.font.Font("assets/fonts/retro_computer_personal_use.ttf", 100)
scores_font = pygame.font.Font("assets/fonts/retro_computer_personal_use.ttf", 20)
victory_font = pygame.font.Font("assets/fonts/SquaredanceFontV1-Regular.ttf", 120)
score = [0, 0] # [player1, player2]
round_finished = False
round_finished_coutdown = 2000

# Draw text display
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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
figther_1 = Fighter(1, 200, bgd_floor, False, samuraiMack_data, samuraiMack_full_sprite, samuraiMack_full_sprites_steps, sword_soundEffect, hit_soundEffect, jump_soundEffect, walk_soundEffect)

# figther_2 = Fighter(500, bgd_floor, True, kenji_data, kenji_full_sprite, kenji_full_sprites_steps, sword_soundEffect, hit_soundEffect, jump_soundEffect, walk_soundEffect)
figther_2 = Fighter(2, 800, bgd_floor, True, samuraiMack_data, samuraiMack_full_sprite, samuraiMack_full_sprites_steps, sword_soundEffect, hit_soundEffect, jump_soundEffect, walk_soundEffect)

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
    draw_text("Player One :" + " " + str(score[0]), scores_font, yellow, 20, 60)
    draw_text("Player Two :" + " " + str(score[1]), scores_font, blue, 580, 60)
    # update the start countdown
    if start_countdown <= 0:
        # manage figthers movement
        figther_1.move(win_x, win_y, floor_height, screen, figther_2, round_finished)
        figther_2.move(win_x, win_y, floor_height, screen, figther_1, round_finished)
    else :
        # count timer display
        draw_text(str(start_countdown), countdown_font, red, win_x/2 , win_y/3)
        # Update the start countdown, we use the last_countdown_update in order to check if the last ticks was for one seconds or more
        if pygame.time.get_ticks() - last_countdown_update >= 1000:
            start_countdown -= 1
            last_countdown_update = pygame.time.get_ticks()
            

    figther_1.update_sprite()
    figther_2.update_sprite()
    # Draw Figthers
    figther_1.drawFigther(screen)
    figther_2.drawFigther(screen)
    
    # Score and victory display
    if round_finished == False :
        if figther_1.alive == False :
            score[1] += 1
            round_finished = True
            round_over_time = pygame.time.get_ticks()
        elif figther_2.alive == False :
            score[0] += 1
            round_finished = True
            round_over_time = pygame.time.get_ticks()
    else :
        if figther_1.alive == False :
            draw_text("Fighter 2 Win", victory_font, blue, win_x - 920, win_y/3)
        elif figther_2.alive == False :
            draw_text("Fighter 1 Win", victory_font, yellow, win_x - 920, win_y/3)
        if pygame.time.get_ticks() - round_over_time > round_finished_coutdown:
            round_finished = False
            start_countdown = 3
            # Reset instances of Figther()
            figther_1 = Fighter(1, 200, bgd_floor, False, samuraiMack_data, samuraiMack_full_sprite, samuraiMack_full_sprites_steps, sword_soundEffect, hit_soundEffect, jump_soundEffect, walk_soundEffect)
            # figther_2 = Fighter(500, bgd_floor, True, kenji_data, kenji_full_sprite, kenji_full_sprites_steps, sword_soundEffect, hit_soundEffect, jump_soundEffect, walk_soundEffect)
            figther_2 = Fighter(2, 800, bgd_floor, True, samuraiMack_data, samuraiMack_full_sprite, samuraiMack_full_sprites_steps, sword_soundEffect, hit_soundEffect, jump_soundEffect, walk_soundEffect)
    
    
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
