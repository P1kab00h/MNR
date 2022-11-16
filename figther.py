import pygame


class Fighter():
    # Constructor
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 50, 150))
        self.velocity_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        
    '''    
    def load_images(self, sprite_sheet, animation_steps):
        for _ in range(animation):
    '''    
 
        
    # Movement handler
    def move(self, screen_width, screen_height, floor_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # listen to key press
        key = pygame.key.get_pressed()

        # All movement bellow is avaible if not attacking
        if self.attacking == False:
            # movement
                # left (x axis)
            if key[pygame.K_q]:
                dx = -SPEED
                # rigth (x axis)
            if key[pygame.K_d]:
                dx = +SPEED
                # jump up / down gravity (y axis)
            if key[pygame.K_z] and self.jump == False:
                self.velocity_y = -30
                self.jump = True
                # attacks
            if key[pygame.K_v] or key[pygame.K_b]:
                
                self.attack(surface, target)
                # Now get the precise attack being used
                if key[pygame.K_v]:
                    self.attack_type = 1
                if key[pygame.K_b]:
                    self.attack_type = 2

        # apply gravity 
        self.velocity_y += GRAVITY
        dy += self.velocity_y

        # keep player onto the screen
        # Left side of th screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        # Right side of the screen, 
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        # Up & Down
        if self.rect.bottom + dy > screen_height - floor_height:
            self.velocity_y = 0
            # The player is on the floor so he can jump again
            self.jump = False
            dy = screen_height - floor_height - self.rect.bottom
        
        
        # Keep player facing each other
        if target.rect.centerx > self.rect.centerx:
            # initial case for player one
            self.flip = False
        else:
            # if player one go over player two position
            self.flip = True
            
        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # Attack Method
    def attack(self, surface, target):
        self.attacking = True
        # self.rect.centerx - (2 * self.rect.width * self.flip)
        # Help determine wich side should be attacked depending on self.flip
        # If True then draw the rectangle on the left side of the player
        attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        # check for collision between attack and the other player
        if attack_rect.colliderect(target.rect):
            print("ouchy Baby")
            target.health -= 10
            print(target.health)
        pygame.draw.rect(surface, (255, 50, 0), attack_rect)
        self.attacking = False
        
    # Draw figther as rectangle
    def drawFigther(self, surface):
        pygame.draw.rect(surface, (255, 0, 250), self.rect)
