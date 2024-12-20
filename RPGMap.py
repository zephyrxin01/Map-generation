from RPGTile import RPGTile
import random
class RPGMap:
    TERRAIN_TYPES = ["0", "1", "2", "3", "4", "5", "6"]  
    """
    "0": RPGTile("mountain.png"),
    "1": RPGTile("river.png"),
    "2": RPGTile("grass.png"),
    "3": RPGTile("rock.png"),
    "4": RPGTile("riverstone.png"),
    "5": RPGTile("rice.png"),
    "6": RPGTile("house.png"),
    """

    def __init__(self, filename=None, width=None, height=None):
        """Initialize map either from file or as an empty grid."""
        if filename:
            self.map = self.load_map(filename)
        elif width and height:
            self.map = [[random.choice(RPGMap.TERRAIN_TYPES) for _ in range(width)] for _ in range(height)]
        else:
            raise ValueError("Provide either a filename or dimensions for the map.")

        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, x, y):
        if y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[0]):
            return RPGTile("empty.png")
        return RPGTile.get_tile(self.map[y][x])
    
    def load_map(self, filename):
        """Load map from a file."""
        with open(filename, "r") as f:
            return [list(line.strip()) for line in f.readlines()]

    def evaluate_fitness(self):
        """Evaluate the fitness of the map."""
        fitness = 0
        river_count = 0
        river_stone = 0
        for y in range(self.height):
            for x in range(self.width):
                tile = self.map[y][x]
                if tile == "1":
                    river_count += 1
                    adjacent_rivers = self.count_adjacent(x, y, "1")
                    if adjacent_rivers < 1:
                        fitness -= 1000
                    elif adjacent_rivers < 2:
                        fitness -= 500
                    elif adjacent_rivers < 3:
                        fitness -= 100
                elif tile == "4":
                    river_stone += 1
                elif tile == "5":
                    adjacent_rivers = self.count_adjacent(x, y, "1")
                    if adjacent_rivers < 2:
                        fitness -= 1000
                elif tile == "6":
                    adjacent_rivers = self.count_adjacent(x, y, "1")
                    if adjacent_rivers < 2:
                        fitness -= 10000
                    elif adjacent_rivers > 2:
                        fitness += 10000
        total_river = river_count + river_stone
        if total_river > 250:
            penalty = (river_count-250)*1000
            fitness -= penalty

        return fitness

    def is_near_tile(self, x, y, tile_type):
        """Check if a specific tile type is adjacent to (x, y)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.map[ny][nx] == tile_type:
                    return True
        return False

    def distance_to_tile(self, x, y, tile_type):
        """Find the shortest distance from (x, y) to the nearest tile of a specific type."""
        from collections import deque

        visited = set()
        queue = deque([(x, y, 0)])  # (current_x, current_y, distance)

        while queue:
            cx, cy, dist = queue.popleft()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            # Check if this tile matches the target type
            if 0 <= cx < self.width and 0 <= cy < self.height and self.map[cy][cx] == tile_type:
                return dist

            # Add neighbors to the queue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    queue.append((nx, ny, dist + 1))

        return float('inf')  # Return a very large number if no tile is found

    
    def flood_fill(self, x, y, tile_type, visited=None):
        """Calculate the size of the connected region of the same tile type."""
        if visited is None:
            visited = set()
        if (x, y) in visited or x < 0 or y < 0 or x >= self.width or y >= self.height:
            return 0
        if self.map[y][x] != tile_type:
            return 0

        visited.add((x, y))
        size = 1  # Current tile
        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            size += self.flood_fill(x + dx, y + dy, tile_type, visited)
        return size

    def check_adjacent(self, x, y, tile_type, reward=0, penalty=0):
        """Check adjacent tiles for a specific type and apply a reward or penalty."""
        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent directions
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.map[ny][nx] == tile_type:
                    count += 1
        return count * reward - (0 if count > 0 else penalty)

    def count_adjacent(self, x, y, tile_type):
        """Count the number of adjacent tiles of a specific type."""
        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.map[ny][nx] == tile_type:
                    count += 1
        return count


    def mutate(self, mutation_rate):
        """Mutate the map with the given mutation rate."""
        for y in range(self.height):
            for x in range(self.width):
                current_tile = self.map[y][x]

                if current_tile == "0" and random.random() < 0.0005:
                    self.map[y][x] = "1"  # Change to river

                elif current_tile == "1" and random.random() < mutation_rate:
                    new_tile = random.choice(["1", "4", "5"])  # Exclude "0" (mountain)
                    self.map[y][x] = new_tile

                elif current_tile == "2" and random.random() < mutation_rate:
                    new_tile = random.choice(["1", "2", "5", "6"]) 
                    self.map[y][x] = new_tile

                elif current_tile == "3" and random.random() < mutation_rate:
                    new_tile = random.choice(["2", "3", "6"]) 
                    self.map[y][x] = new_tile

                elif current_tile == "4" and random.random() < mutation_rate:
                    self.map[y][x] = "1"  # Change to river

                elif current_tile == "5" and random.random() < mutation_rate:
                    self.map[y][x] = "2"  # Change to grass

                # 7. If the current tile is "6" (house), it has probability n to change to any tile except "0"
                elif current_tile == "6" and random.random() < mutation_rate:
                    new_tile = random.choice(["1", "2", "3", "4", "5", "6"])  # Exclude "0" (mountain)
                    self.map[y][x] = new_tile

    @staticmethod
    def crossover(map1, map2):
        """Combine two maps to produce a child map."""
        child = RPGMap(width=map1.width, height=map1.height)
        for y in range(map1.height):
            for x in range(map1.width):
                child.map[y][x] = map1.map[y][x] if random.random() > 0.5 else map2.map[y][x]
        return child
