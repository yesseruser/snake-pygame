from enum import Enum
import pygame

TILE_SIZE = 50
TILE_COUNT = 12
SPEED = 5

pygame.init()
win = pygame.display.set_mode((TILE_COUNT * TILE_SIZE, TILE_COUNT * TILE_SIZE))
clock = pygame.time.Clock()


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


class Player:
    body: list[pygame.Vector2]
    current_direction: Direction
    next_direction: Direction

    def __init__(self, x, y):
        self.body = [pygame.Vector2(x, y)]
        self.current_direction = Direction.Nothing
        self.next_direction = Direction.Nothing

    def head(self) -> pygame.Vector2:
        return self.body[0]

    def update(self):
        previous_pos = self.head()
        self.body[0] = self.current_direction.apply(self.head(), SPEED)
        for i in range(1, len(self.body)):
            new_previous_pos = self.body[i]
            self.body[i] = previous_pos
            previous_pos = new_previous_pos

        if (
            self.head().x % TILE_SIZE == 0
            and self.head().y % TILE_SIZE == 0
            and self.next_direction != Direction.Nothing
        ):
            self.current_direction = self.next_direction
            self.next_direction = Direction.Nothing

    def draw(self):
        for part in self.body:
            pygame.draw.rect(win, (0, 200, 0), (part.x, part.y, TILE_SIZE, TILE_SIZE))


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


player = Player((TILE_COUNT // 2) * TILE_SIZE, (TILE_COUNT // 2) * TILE_SIZE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.update()

    win.fill((10, 10, 10))
    draw_grid()
    player.draw()

    pygame.display.flip()

    clock.tick(60)
