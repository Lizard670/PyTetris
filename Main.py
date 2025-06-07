import pygame
import os
from random import shuffle


class Game:
    def __init__(self, skin, config):
        self.skin_config = skin
        self.cooldowns_times = config["cooldowns"]

        self.tetrominoes = []
        # I tetromino
        self.tetrominoes.append([[[0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 0, 0]],
                                 [[0, 0, 0, 0],
                                  [1, 1, 1, 1],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]],
                                 [[0, 0, 1, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 1, 0]],
                                 [[0, 0, 0, 0],
                                  [0, 0, 0, 0],
                                  [1, 1, 1, 1],
                                  [0, 0, 0, 0]]])
        # O tetromino
        self.tetrominoes.append([[[1, 1],
                                  [1, 1]],
                                 [[1, 1],
                                  [1, 1]],
                                 [[1, 1],
                                  [1, 1]],
                                 [[1, 1],
                                  [1, 1]]])
        # T tetromino
        self.tetrominoes.append([[[0, 1, 0],
                                  [1, 1, 0],
                                  [0, 1, 0]],
                                 [[0, 1, 0],
                                  [1, 1, 1],
                                  [0, 0, 0]],
                                 [[0, 1, 0],
                                  [0, 1, 1],
                                  [0, 1, 0]],
                                 [[0, 0, 0],
                                  [1, 1, 1],
                                  [0, 1, 0]]])
        # L tetromino
        self.tetrominoes.append([[[0, 1, 0],
                                  [0, 1, 0],
                                  [0, 1, 1]],
                                 [[0, 0, 0],
                                  [1, 1, 1],
                                  [1, 0, 0]],
                                 [[1, 1, 0],
                                  [0, 1, 0],
                                  [0, 1, 0]],
                                 [[0, 0, 1],
                                  [1, 1, 1],
                                  [0, 0, 0]]])
        # J tetromino
        self.tetrominoes.append([[[0, 1, 0],
                                  [0, 1, 0],
                                  [1, 1, 0]],
                                 [[1, 0, 0],
                                  [1, 1, 1],
                                  [0, 0, 0]],
                                 [[0, 1, 1],
                                  [0, 1, 0],
                                  [0, 1, 0]],
                                 [[0, 0, 0],
                                  [1, 1, 1],
                                  [0, 0, 1]]])
        # Z tetromino
        self.tetrominoes.append([[[0, 1, 0],
                                  [1, 1, 0],
                                  [1, 0, 0]],
                                 [[1, 1, 0],
                                  [0, 1, 1],
                                  [0, 0, 0]],
                                 [[0, 0, 1],
                                  [0, 1, 1],
                                  [0, 1, 0]],
                                 [[0, 0, 0],
                                  [1, 1, 0],
                                  [0, 1, 1]]])
        # S tetromino
        self.tetrominoes.append([[[1, 0, 0],
                                  [1, 1, 0],
                                  [0, 1, 0]],
                                 [[0, 1, 1],
                                  [1, 1, 0],
                                  [0, 0, 0]],
                                 [[0, 1, 0],
                                  [0, 1, 1],
                                  [0, 0, 1]],
                                 [[0, 0, 0],
                                  [0, 1, 1],
                                  [1, 1, 0]]])

        # Create game matrix
        self.matrix = []
        for y in range(20):
            self.matrix.append([])
            for x in range(10):
                self.matrix[y].append(-1)

        # Tetrominoes setup
        self.queue = [0, 1, 2, 3, 4, 5, 6]
        shuffle(self.queue)
        self.next_index = 0

        self.current_tetromino = -1
        self.holding = -1
        self.can_hold = True
        self.tetromino_rotation = 0
        self.tetromino_position = [0, 0]
        self.next_tetromino()

        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((575, 720))
        clock = pygame.time.Clock()
        cooldowns = {}
        for key, time in self.cooldowns_times.items():
            cooldowns[key] = 0
        running = True
        self.screen_changed = True

        # load background
        screen.fill(skin_config["back_color"])
        self.background = pygame.image.load(os.path.join(skin_config["path"], 'background.png')).convert()

        # main game loop
        while running:
            # poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_s | pygame.K_DOWN:
                            if self.move(0, -1):
                                cooldowns["vertical"] = self.cooldowns_times["vertical"]

                        case pygame.K_a | pygame.K_LEFT:
                            if self.move(-1, 0):
                                cooldowns["horizontal"] = self.cooldowns_times["horizontal"]
                        case pygame.K_d | pygame.K_RIGHT:
                            if self.move(1, 0):
                                cooldowns["horizontal"] = self.cooldowns_times["horizontal"]

                        case pygame.K_w | pygame.K_UP:
                            if self.rotate(1):
                                cooldowns["spin"] = self.cooldowns_times["spin"]
                        case pygame.K_c:
                            if self.can_hold:
                                self.hold()

            # place the background on top of whatever was in the screen
            screen.blit(self.background, (0, 0))

            if self.screen_changed:
                self.draw(screen)
                pygame.display.flip()
                self.screen_changed = False

            # Tetromino natural fall
            if cooldowns["fall"] <= 0:
                if self.move(0, -1):
                    cooldowns["vertical"] = self.cooldowns_times["vertical"]
                    cooldowns["fall"] = self.cooldowns_times["fall"]
                else:
                    self.set_tetromino()

            # Detects player controls
            keys = pygame.key.get_pressed()

            if cooldowns["drop"] <= 0:
                if keys[pygame.K_SPACE]:
                    while self.move(0, -1):
                        pass
                    self.set_tetromino()
                    cooldowns["drop"] = self.cooldowns_times["drop"]

            if cooldowns["vertical"] <= 0:
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    if self.move(0, -1):
                        cooldowns["vertical"] = self.cooldowns_times["vertical"]
                        cooldowns["fall"] = self.cooldowns_times["fall"]

            if cooldowns["horizontal"] <= 0:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    if self.move(-1, 0):
                        cooldowns["horizontal"] = self.cooldowns_times["horizontal"]
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    if self.move(1, 0):
                        cooldowns["horizontal"] = self.cooldowns_times["horizontal"]

            # limits FPS to 60s
            # dt = ms since last loop
            dt = clock.tick()
            for key, time in self.cooldowns_times.items():
                cooldowns[key] -= dt

        pygame.quit()

    # Update the current tetromino to be the next in queue
    def next_tetromino(self):
        # gets the new tetromino and sets the next index
        self.current_tetromino = self.queue[self.next_index]
        self.next_index += 1

        self.reset_position()
        # if the index get past 6 means that we need to reset the list
        if self.next_index > 6:
            shuffle(self.queue)
            self.next_index = 0

    def hold(self):
        if self.holding == -1:
            self.holding = self.current_tetromino
            self.next_tetromino()
        else:
            temp = self.holding
            self.holding = self.current_tetromino
            self.current_tetromino = temp
        self.can_hold = False
        self.reset_position()

    def reset_position(self):
        # resets rotation
        self.tetromino_rotation = 0
        # resets position
        size = len(self.tetrominoes[self.current_tetromino][0])
        #    place the tetromino above the matrix to check if it has space or the player have lost the game
        #    + 0.2 to correct float imprecision
        self.tetromino_position = [int(6 - round(size / 2 + 0.2)), 20]
        self.move(0, -size)

    def move(self, x, y):
        if self.check_position((self.tetromino_position[0] + x, self.tetromino_position[1] + y)):
            self.tetromino_position[0] += x
            self.tetromino_position[1] += y
            self.screen_changed = True
            return True
        else:
            return False

    def rotate(self, direction):
        # applies rotation
        r = self.tetromino_rotation + direction
        r = r if 0 <= r else 3
        r = r if r < 4 else 0
        self.tetromino_rotation = r
        # Checks if its valid
        for x in [0, -1, 1]:
            for y in [0, -1, 1]:
                if self.move(x, y):
                    return True

        # Undo rotation
        r = self.tetromino_rotation - direction
        r = r if 0 <= r else 3
        r = r if r < 4 else 0
        self.tetromino_rotation = r
        return False

    def check_position(self, position):
        tetromino = self.current_tetromino
        tetromino_size = len(self.tetrominoes[tetromino][self.tetromino_rotation])

        for y in range(tetromino_size):
            real_y = position[1] + y
            for x in range(tetromino_size):
                real_x = position[0] + x
                if self.tetrominoes[tetromino][self.tetromino_rotation][y][x]:
                    if (0 <= real_x < 10) and (real_y >= 0):
                        if 20 > real_y:
                            if self.matrix[real_y][real_x] != -1:
                                return False
                    else:
                        return False
        return True

    def set_tetromino(self):
        tetromino = self.current_tetromino
        tetromino_size = len(self.tetrominoes[tetromino][self.tetromino_rotation])
        full_lines = []
        for y in range(tetromino_size):
            real_y = self.tetromino_position[1] + y
            for x in range(tetromino_size):
                real_x = self.tetromino_position[0] + x
                if self.tetrominoes[tetromino][self.tetromino_rotation][y][x]:
                    self.matrix[real_y][real_x] = self.skin_config["colors"][self.current_tetromino]
            if 0 <= real_y < 20:
                full_line = True
                for cell in self.matrix[real_y]:
                    if cell == -1:
                        full_line = False
                        break
                if full_line:
                    full_lines.append(real_y)
        for line in reversed(full_lines):
            del self.matrix[line]
            self.matrix.append([])
            for i in range(10):
                self.matrix[19].append(-1)
            print(self.matrix)

        self.next_tetromino()
        self.can_hold = True

    def draw(self, screen):
        size = self.skin_config["block_size"]
        gap = self.skin_config["block_gap"]

        # draws the current tetromino
        tetromino = self.current_tetromino
        tetromino_size = len(self.tetrominoes[tetromino][self.tetromino_rotation])
        for y in range(tetromino_size):
            real_y = self.tetromino_position[1] + y
            for x in range(tetromino_size):
                real_x = self.tetromino_position[0] + x
                if (0 <= real_x < 10) and (0 <= real_y < 20):
                    if self.tetrominoes[tetromino][self.tetromino_rotation][y][x]:
                        self.draw_block(screen, real_x, real_y, size, gap, self.skin_config["colors"][tetromino])
        # draws current tetromino shadow
        # TODO

        # offsets to perfect fit into holding e next boxes
        offsets = [(-0.5, 0), (0, -1), (0, -0.5), (-1, -0.5), (0, -0.5), (0, -0.5), (0, -0.5)]
        # tetromino holding
        if self.holding != -1:
            tetromino_size = len(self.tetrominoes[self.holding][0])
            for y in range(-tetromino_size, 0):
                real_y = self.skin_config["hold_position"][1] + y + offsets[self.holding][1]
                for x in range(tetromino_size):
                    real_x = self.skin_config["hold_position"][0] + x + offsets[self.holding][0]
                    if self.tetrominoes[self.holding][0][y][x]:
                        self.draw_block(screen, real_x, real_y, size, gap, self.skin_config["colors"][self.holding])

        # next tetromino
        next_type = self.queue[self.next_index]
        tetromino_size = len(self.tetrominoes[next_type][0])
        for y in range(-tetromino_size, 0):
            real_y = self.skin_config["next_position"][1] + y + offsets[next_type][1]
            for x in range(tetromino_size):
                real_x = self.skin_config["next_position"][0] + x + offsets[next_type][0]
                if self.tetrominoes[next_type][0][y][x]:
                    self.draw_block(screen, real_x, real_y, size, gap, self.skin_config["colors"][next_type])

        # draws game matrix
        matrix_height = len(self.matrix)
        matrix_width = len(self.matrix[0])
        for y in range(matrix_height):
            for x in range(matrix_width):
                if not self.matrix[y][x] == -1:
                    self.draw_block(screen, x, y, size, gap, self.matrix[y][x])

    def draw_block(self, screen, x, y, size, gap, color):
        rect = pygame.Rect(self.skin_config["matrix_position"][0] + x * (size + gap),
                           self.skin_config["matrix_position"][1] + (19 - y) * (size + gap),
                           size, size)
        pygame.draw.rect(screen, color, rect)


if __name__ == '__main__':
    skin_config = {"path": "images",
                   "back_color": "#4D5C63",
                   "block_size": 28,
                   "block_gap": 2,
                   "matrix_position": (140, 51),
                   "hold_position": (-3, 15),
                   "next_position": (11, 15),
                   "colors": ["#0F9BD7", "#E39F02", "#AF298A", "#2141C6", "#E35B02", "#59B101", "#D70F37"]}

    game_config = {"cooldowns": {"horizontal": 100,
                                 "vertical": 50,
                                 "drop": 200,
                                 "fall": 750,
                                 "spin": 200}}

    game = Game(skin_config, game_config)
