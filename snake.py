import pygame
import random

pygame.init()


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 1
        self.speed_y = 0
        segments = []
        for a in range(1, 4):
            segments.append(Segment(self.x - a, self.y))
        self.segments = segments

    def move(self):
        global score, game_mode
        # handle key inputs
        keys = pygame.key.get_pressed()
        for key in keys:
            if self.speed_x == 0:
                if keys[pygame.K_a]:
                    self.speed_x = -1
                    self.speed_y = 0
                if keys[pygame.K_d]:
                    self.speed_x = 1
                    self.speed_y = 0
            elif self.speed_y == 0:
                if keys[pygame.K_w]:
                    self.speed_x = 0
                    self.speed_y = -1
                if keys[pygame.K_s]:
                    self.speed_x = 0
                    self.speed_y = 1

        # check for wall collisions
        if self.x + self.speed_x < 0 or self.x + self.speed_x > rows - 1 or self.y + self.speed_y > rows - 1 or \
                self.y + self.speed_y < 0:
            game_mode = "end"
            start.text = "RETRY"
            return None

        # moves snake
        self.segments.insert(0, Segment(self.x, self.y))
        self.x += self.speed_x
        self.y += self.speed_y

        # checks for self collisions
        for segment in self.segments:
            if self.x == segment.x and self.y == segment.y and self.segments.index(segment)!=len(self.segments)-1:
                game_mode = "end"
                start.text = "RETRY"
                break

        # checks for eating food
        if self.x == food.x and self.y == food.y:
            for a in range(0, len(self.segments)):
                segment = self.segments[a]
                food.x = random.randrange(0, 16)
                food.y = random.randrange(0, 16)
                if food.x == segment.x and food.y == segment.y:
                    a -= 1
            score += 1
        else:
            self.segments.pop()

    def draw(self):
        for segment in self.segments:
            segment.draw()
        pygame.draw.rect(screen, (255, 0, 0), (self.x * size / rows, self.y * size / rows, size / rows, size / rows))


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, (0, 255 - player.segments.index(self), 0),
                         (self.x * size / rows, self.y * size / rows, size / rows, size / rows))


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), (self.x * size / rows, self.y * size / rows, size / rows, size / rows))


class button:
    def __init__(self, x, y, r, g, b, text, font, width, height):
        self.x = x
        self.y = y
        self.r = r
        self.b = b
        self.g = g
        self.text = text
        self.font = font
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, (self.r, self.g, self.b), (self.x, self.y, self.width, self.height))
        screen.blit(self.font.render(self.text, False, (0, 100, 0)), (self.x + 10, self.y))

    def mouse_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True


def draw_grid():
    margin = size / rows
    x = 0
    y = 0
    for line in range(rows):
        x = x + margin
        y = y + margin

        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, size))
        pygame.draw.line(screen, (255, 255, 255), (0, y), (size, y))


def render_screen():
    screen.fill((0, 0, 0))
    draw_grid()
    player.move()
    player.draw()
    food.draw()
    screen.fill((0, 0, 0), (0, 513, 512, 50))
    start.draw()
    screen.blit(comic_font.render('Score: ' + str(score), False, (255, 100, 0)), (10, size + 5))
    pygame.display.update()


size = 512
rows = 16

screen = pygame.display.set_mode((size, size + 50))
pygame.display.set_caption("Snake")

comic_font = pygame.font.SysFont("Comic Sans MS", 30)

clock = pygame.time.Clock()

running = True
game_mode = "wait"

player = Snake(8, 8)
food = Food(random.randrange(0, 16), random.randrange(0, 16))
start = button(size - 155, size + 5, 0, 255, 0, "PLAY", comic_font, 150, 40)

score = 0

render_screen()

while running:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start.mouse_over(pos):
                if game_mode == "wait":
                    game_mode = "play"
                    start.text = "PAUSE"
                elif game_mode == "play":
                    game_mode = "wait"
                    start.text = "RESUME"
                elif game_mode == "end":
                    game_mode = "play"
                    start.text = "PAUSE"
                    score = 0
                    running = True
                    game_mode = "wait"
                    player = Snake(8, 8)
                    food = Food(random.randrange(0, 16), random.randrange(0, 16))
                render_screen()
    if game_mode == "play":
        pygame.time.delay(0)
        clock.tick(7)
        render_screen()
