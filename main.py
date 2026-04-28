# 1. mřížka
# 2. hráč (pohyb bez zahnutí)
# 3. jablka
# 4. hráč (pohyb se zahnutím - normálně)

import random
from enum import Enum
import pygame

TILE_SIZE = 50
TILE_COUNT = 12
SPEED = 5


class Direction(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3
    Nothing = 4

    def apply(self, vector: pygame.Vector2, increment=1) -> pygame.Vector2:
        match self:
            case Direction.Up:
                return pygame.Vector2(vector.x, vector.y - increment)
            case Direction.Down:
                return pygame.Vector2(vector.x, vector.y + increment)
            case Direction.Left:
                return pygame.Vector2(vector.x - increment, vector.y)
            case Direction.Right:
                return pygame.Vector2(vector.x + increment, vector.y)
            case _:
                return pygame.Vector2(vector.x, vector.y)

    def invert(self) -> Direction:
        match self:
            case Direction.Up:
                return Direction.Down
            case Direction.Down:
                return Direction.Up
            case Direction.Left:
                return Direction.Right
            case Direction.Right:
                return Direction.Left
            case _:
                return Direction.Nothing


class SnakePart:
    position: pygame.Vector2
    direction: Direction

    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.direction = Direction.Nothing

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position, (TILE_SIZE, TILE_SIZE))

    def draw(self):
        pygame.draw.rect(
            win, (0, 200, 0), (self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        )

    def update(self):
        if self.direction != Direction.Nothing:
            self.position = self.direction.apply(self.position, SPEED)

    def eat_apple(self, apples: list[Apple]) -> bool:
        for i, apple in enumerate(apples):
            if self.rect().colliderect(apple.rect()):
                apples[i] = Apple()
                return True
        return False


class Player:
    body: list[SnakePart]
    next_direction: Direction

    def __init__(self, x, y):
        self.body = [
            SnakePart(x, y),
            SnakePart(x - TILE_SIZE, y),
            SnakePart(x - (2 * TILE_SIZE), y),
        ]
        self.next_direction = Direction.Nothing

    def head(self) -> SnakePart:
        return self.body[0]

    def update(self):
        for part in self.body:
            part.update()

        if (
            self.head().position.x % TILE_SIZE == 0
            and self.head().position.y % TILE_SIZE == 0
            and self.next_direction != Direction.Nothing
        ):  # kombinace for part in self.body a for i in range(len(self.body))
            for i, part in enumerate(self.body):
                part.direction = self.next_direction
            self.next_direction = Direction.Nothing

        if self.head().eat_apple(apples):
            pos = (
                self.body[-1]
                .direction.invert()
                .apply(self.body[-1].position, TILE_SIZE)
            )
            part = SnakePart(pos.x, pos.y)
            part.direction = self.body[-1].direction
            self.body.append(part)

    def draw(self):
        for part in self.body:
            part.draw()


class Apple:
    position: pygame.Vector2

    def __init__(self):
        x = random.randint(0, TILE_COUNT - 1) * TILE_SIZE
        y = random.randint(0, TILE_COUNT - 1) * TILE_SIZE
        self.position = pygame.Vector2(x, y)

    def draw(self):
        pygame.draw.circle(
            win,
            (255, 0, 0),
            self.position + pygame.Vector2(TILE_SIZE / 2, TILE_SIZE / 2),
            TILE_SIZE / 2,
        )

    def rect(self):
        return pygame.Rect(self.position, (TILE_SIZE, TILE_SIZE))


def draw_grid():
    for x in range(0, TILE_COUNT):
        for y in range(0, TILE_COUNT):
            if y % 2 == 0:
                if x % 2 == 0:
                    pygame.draw.rect(
                        win,
                        (40, 40, 40),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )
            else:
                if (x - 1) % 2 == 0:
                    pygame.draw.rect(
                        win,
                        (40, 40, 40),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )


pygame.init()
win = pygame.display.set_mode((TILE_COUNT * TILE_SIZE, TILE_COUNT * TILE_SIZE))
clock = pygame.time.Clock()

player = Player((TILE_COUNT // 2) * TILE_SIZE, (TILE_COUNT // 2) * TILE_SIZE)
apples = [Apple()]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player.head().direction != Direction.Down:
                player.next_direction = Direction.Up
            if event.key == pygame.K_DOWN and player.head().direction != Direction.Up:
                player.next_direction = Direction.Down
            if (  # tohle mě odsazuje LSP
                event.key == pygame.K_LEFT
                and player.head().direction != Direction.Right
            ):
                player.next_direction = Direction.Left
            if (
                event.key == pygame.K_RIGHT
                and player.head().direction != Direction.Left
            ):
                player.next_direction = Direction.Right

    player.update()

    win.fill((10, 10, 10))
    draw_grid()
    player.draw()
    for apple in apples:
        apple.draw()

    pygame.display.flip()

    clock.tick(60)
