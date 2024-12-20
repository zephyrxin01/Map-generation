import pygame

class RPGTile:
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, image_file):
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (RPGTile.WIDTH, RPGTile.HEIGHT))

    @staticmethod
    def get_tile(tile_type):
        tile_map = {
            "0": RPGTile("mountain.png"),
            "1": RPGTile("river.png"),
            "2": RPGTile("grass.png"),
            "3": RPGTile("rock.png"),
            "4": RPGTile("riverstone.png"),
            "5": RPGTile("rice.png"),
            "6": RPGTile("house.png"),
        }
        return tile_map.get(tile_type, RPGTile("empty.png"))
