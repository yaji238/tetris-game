import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
PLAY_AREA_WIDTH = 300
PLAY_AREA_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, ORANGE, BLUE]

# Game variables
grid = [[BLACK for _ in range(10)] for _ in range(20)]
score = 0
level = 0
lines_cleared = 0

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        # Handle case where line is a list or an integer
        if isinstance(line, list):
            row = line
        else:
            # If it's a single integer, make it into a list with one element
            row = [line]

        for j, column in enumerate(row):
            if column == 1:
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == BLACK] for y in range(20)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Shape(5, 0, random.choice(SHAPES))

class Shape:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def draw_text_middle(text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    screen.blit(label, (SCREEN_WIDTH/2 - label.get_width()/2, SCREEN_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, WHITE, (0, i*30), (SCREEN_WIDTH, i*30))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, WHITE, (j*30, 0), (j*30, SCREEN_HEIGHT))

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, WHITE)

    start_x = SCREEN_WIDTH + 50
    start_y = SCREEN_HEIGHT/2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 1:
                pygame.draw.rect(surface, shape.color,
                                 (start_x + j*30, start_y + i*30, 30, 30), 0)

    surface.blit(label, (start_x + 10, start_y - 30))

def draw_window(surface, grid):
    surface.fill(BLACK)

    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, WHITE)

    surface.blit(label, (SCREEN_WIDTH/2 - label.get_width()/2, 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (SCREEN_WIDTH/2 - 150 + j*30, SCREEN_HEIGHT/2 - 300 + i*30, 30, 30), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 300,
                                       PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT), 4)

def main():
    global grid

    locked_positions = {}
    shape = get_shape()
    next_shape = get_shape()

    run = True
    fall_time = 0
    lines_cleared = 0
    score = 0
    level = 1

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        # Increase speed as level increases
        if lines_cleared > 0 and lines_cleared % 10 == 0:
            level += 1
            fall_speed *= 0.9

        # Increase score as lines cleared increases
        if lines_cleared > 0 and lines_cleared % 5 == 0:
            score += 10

        # Game logic
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            shape.y += 1
            if not valid_space(shape, grid) and shape.y > 0:
                shape.y -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape.x -= 1
                    if not valid_space(shape, grid):
                        shape.x += 1

                elif event.key == pygame.K_RIGHT:
                    shape.x += 1
                    if not valid_space(shape, grid):
                        shape.x -= 1

                elif event.key == pygame.K_DOWN:
                    shape.y += 1
                    if not valid_space(shape, grid):
                        shape.y -= 1

                elif event.key == pygame.K_UP:
                    shape.rotate()
                    if not valid_space(shape, grid):
                        shape.rotation = (shape.rotation - 1) % len(shape.shape)

        shape_positions = convert_shape_format(shape)

        for i in range(len(shape_positions)):
            x, y = shape_positions[i]
            if y > -1:
                grid[y][x] = shape.color

        # Check if shape has landed
        if not valid_space(shape, grid):
            shape.y -= 1
            for pos in shape_positions:
                p = (pos[0], pos[1])
                locked_positions[p] = shape.color

            # Clear rows and update score
            lines_cleared += clear_rows(grid, locked_positions)
            score += 10

            # Generate new shape
            shape = next_shape
            next_shape = get_shape()

            if check_lost(locked_positions):
                run = False

        draw_window(screen, grid)
        pygame.display.update()

    draw_text_middle("YOU LOST", 80, RED)
    pygame.display.update()
    pygame.time.delay(1500)

if __name__ == "__main__":
    main()