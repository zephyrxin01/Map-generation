from RPGTile import RPGTile
class RPGView:
    RADIUS = 8  # 可見區域半徑

    def __init__(self, avatar, map_data, screen):
        self.avatar = avatar
        self.map_data = map_data
        self.screen = screen
        self.margin_x = (screen.get_width() - RPGTile.WIDTH * (self.RADIUS * 2 + 1)) // 2
        self.margin_y = (screen.get_height() - RPGTile.HEIGHT * (self.RADIUS * 2 + 1)) // 2

    def move_avatar(self, direction):
        new_x, new_y = self.avatar.x, self.avatar.y
        if direction == "UP":
            new_y -= 1
        elif direction == "DOWN":
            new_y += 1
        elif direction == "LEFT":
            new_x -= 1
        elif direction == "RIGHT":
            new_x += 1

        if 0 <= new_x < len(self.map_data.map[0]) and 0 <= new_y < len(self.map_data.map):
            tile = self.map_data.get_tile(new_x, new_y)
            if tile.image != "mountain.png" and tile.image != "rock.png" and tile.image != "riverstone.png":  # 例如：角色不能走上山地
                self.avatar.x, self.avatar.y = new_x, new_y

    def draw(self):
        x_min = self.avatar.x - self.RADIUS
        y_min = self.avatar.y - self.RADIUS

        for dx in range(-self.RADIUS, self.RADIUS + 1):
            for dy in range(-self.RADIUS, self.RADIUS + 1):
                tile = self.map_data.get_tile(x_min + dx, y_min + dy)
                self.screen.blit(
                    tile.image,
                    (self.margin_x + (dx + self.RADIUS) * RPGTile.WIDTH,
                     self.margin_y + (dy + self.RADIUS) * RPGTile.HEIGHT)
                )
        # 繪製角色
        self.screen.blit(
            self.avatar.image,
            (self.margin_x + self.RADIUS * RPGTile.WIDTH,
             self.margin_y + self.RADIUS * RPGTile.HEIGHT)
        )
