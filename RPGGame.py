import pygame
from RPGMap import RPGMap
from RPGAvatar import RPGAvatar
from RPGView import RPGView
from RPGTile import RPGTile
from GA import GeneticAlgorithm

class RPGGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("RPG Game")
        self.clock = pygame.time.Clock()

        # Initialize Genetic Algorithm with default map
        ga = GeneticAlgorithm(default_map_filename="default.map", population_size=20)
        target_generations = [1, 5, 10, 30, 50, 75, 100, 150, 200, 250, 300]
        previous_gen = 0
        for i in range (len(target_generations)):
            current_gen = target_generations[i]
            self.map = ga.evolve(generations=current_gen-previous_gen, mutation_rate=0.001)
            self.save_map_to_jpg("final_generated_map {}.jpg".format(current_gen))
            previous_gen = current_gen

        # Initialize avatar and view
        self.avatar = RPGAvatar(self.map.width // 2, self.map.height // 2)  # Start in the center
        self.view = RPGView(self.avatar, self.map, self.screen)


    def save_map_to_jpg(self, filename="final_generated_map.jpg"):
        """Render the map using RPGTile images and save as a JPG."""
        tile_width = RPGTile.WIDTH
        tile_height = RPGTile.HEIGHT
        map_width = self.map.width * tile_width
        map_height = self.map.height * tile_height

        # Create a Pygame surface for the entire map
        map_surface = pygame.Surface((map_width, map_height))

        for y in range(self.map.height):
            for x in range(self.map.width):
                tile_type = self.map.map[y][x]
                tile = RPGTile.get_tile(tile_type)  # Get the RPGTile object for this tile type
                map_surface.blit(tile.image, (x * tile_width, y * tile_height))

        # Save the Pygame surface as an image file
        pygame.image.save(map_surface, filename)
        print(f"Map saved as {filename}")

        
    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.view.move_avatar("UP")
                    elif event.key == pygame.K_DOWN:
                        self.view.move_avatar("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.view.move_avatar("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.view.move_avatar("RIGHT")

            self.view.draw()
            pygame.display.flip()
            self.clock.tick(10)  # Limit frame rate

        pygame.quit()


if __name__ == "__main__":
    game = RPGGame()
    game.run()
