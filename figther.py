import pygame


class Fighter():
    # Constructor
    def __init__(self, x, y, data, idle_sprite, idle_steps):
        self.size = data[0]
        self.image_scale = data[2]
        self.offset = data[3]
        self.flip = False
        self.animation_list = self.load_images(idle_sprite, idle_steps)
        self.action = 0 # 0 -> idle ; 1 -> run ; 2 -> jump ; 3 -> attack1 ; 4 -> attack2 ; 5 -> hit ; 6 -> death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 50, 150))
        self.velocity_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        

    def load_images(self, idle_sprite, idle_steps):
        # ectrating all the images from on sprite animation
        animation_list = []
        temp_img_list = []
        for x in range(idle_steps):
            # 10316, to iterate on each single sprite
            temp_img = idle_sprite.subsurface(x * self.size, 0, self.size, self.size)
            temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
        animation_list.append(temp_img_list)
        # print(animation_list)
        return animation_list


        
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
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 250), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
