import pygame
from RPGTile import RPGTile

class RPGAvatar:
    def __init__(self, x, y, image_file="avatar.png"):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (RPGTile.WIDTH, RPGTile.HEIGHT))
