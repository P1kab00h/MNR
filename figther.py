import pygame


class Fighter():
    # Constructor
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 50, 150))
    # Movement handler

    def move(self, screen_width):
        SPEED = 10
        dx = 0
        dy = 0

        # listen to key press
        key = pygame.key.get_pressed()

        # movement
        if key[pygame.K_q]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = +SPEED

        # keep player onto the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # Draw figther as rectangle
    def drawFigther(self, surface):
        pygame.draw.rect(surface, (255, 0, 250), self.rect)
