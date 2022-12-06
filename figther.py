import pygame


class Fighter():
    # Constructor
    def __init__(self, x, y, flip, data, sprite_sheet, sprite_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, sprite_steps)
        self.action = 3 ###### #0-> atck1, #1-> atck2, #2-> death, #3-> idle, #4-> jump, #5-> run, #6 ->take hit
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_sprite_time = pygame.time.get_ticks() # give to a Figther() instance a time stamp at the creation
        self.rect = pygame.Rect((x, y, 50, 150))
        self.velocity_y = 0
        self.runing = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.cooldown_attack = 0
        self.hit = False
        self.health = 10
        self.alive = True
        

    def load_images(self, sprite_sheet, sprite_steps):
        # extracting all the images from on sprite animation
        # y = 0
        animation_list = []
        for y, animation in enumerate(sprite_steps):
            temp_img_list = []
            for x in range(animation):
                # to iterate on each single sprite
                temp_img = sprite_sheet.subsurface(self.size * x, self.size * y, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
            print(animation_list)
        return animation_list
            # y += 1 ==> similaire au comportement obtenu avec enumerate


        
    # Movement handler
    def move(self, screen_width, screen_height, floor_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        # reset self.runing => go back to idle sprite, self.action = 3
        self.runing = False
        self.attack_type = 0

        # listen to key press
        key = pygame.key.get_pressed()

        # All movement bellow is avaible if not attacking
        if self.attacking == False:
            # movement
                # left (x axis)
            if key[pygame.K_q]:
                dx = -SPEED
                self.runing = True
                # rigth (x axis)
            if key[pygame.K_d]:
                dx = +SPEED
                self.runing = True
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
                    self.attacking = True
                if key[pygame.K_b]:
                    self.attack_type = 2
                    self.attacking = True


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
        
        # 
        if self.cooldown_attack > 0:
            self.cooldown_attack -= 1
        
        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # Dealing with sprites updates
    def update_sprite(self):
        # Check the player action's
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(2) # death
        elif self.hit == True:
            self.update_action(6) # Hit
        if self.attacking == True:
            if self.attack_type == 1:
                self.update_action(0) # attack 1
            elif self.attack_type == 2:
                self.update_action(1) # attack 2
        elif self.jump == True:
            self.update_action(4) # jump
        elif self.runing == True:
            self.update_action(5) # runing
        else:
            self.update_action(3) # idle
        # create a cooldown value in order to change sprite each 100 ms
        animation_cooldown = 100
        # to 'animate' the Figther we gonna need to go thru the self.frame_index, doing so will change the self.image for each new index reached
        self.image = self.animation_list[self.action][self.frame_index]
        # if statement to check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_sprite_time > animation_cooldown:
            self.frame_index += 1
            self.update_sprite_time = pygame.time.get_ticks()
        # Check if the sprite array has reach the end, if so go back to the beginning
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
            # check if an attack was (fully) executed
            if self.action == 0 or self.action == 1:
                self.attacking = False # avoid the infinit attack
                self.cooldown_attack = 20
            # check if hit was taken
            if self.action == 6:
                self.hit = False
                # if the opponent was in a middle of an attack ==> the parry (attack stop)
                self.attacking = False
                self.cooldown_attack = 20

    # Attack Method
    def attack(self, surface, target):
        if self.cooldown_attack == 0:
            self.attacking = True
            # ==> self.rect.centerx - (2 * self.rect.width * self.flip)
            # Help determine wich side should be attacked depending on self.flip
            # If True then draw the rectangle on the left side of the player
            attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            # check for collision between attack and the other player
            if attack_rect.colliderect(target.rect):
                print("ouchy Baby")
                target.health -= 10
                target.hit = True
                print(target.health)
            pygame.draw.rect(surface, (255, 50, 0), attack_rect)
            self.attacking = False

    # Handle the out of range animation behaviour
    def update_action(self, new_action):
        # check if the new action is diff then the previous
        if new_action != self.action:
            self.action = new_action    
            # Then update the animation (reset the frame index)
            self.frame_index = 0
            self.update_sprite_time = pygame.time.get_ticks()

    # Draw figther as rectangle(old), now draw the figther and check if he is facing the rigth side
    def drawFigther(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 250), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
