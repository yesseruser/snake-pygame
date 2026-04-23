import pygame

pygame.init()
win = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()


def draw_grid():
    for x in range(0, 600, 50):
        for y in range(0, 600, 50):
            if y % 100 == 0:
                if x % 100 == 0:
                    pygame.draw.rect(win, (40, 40, 40), (x, y, 50, 50))
            else:
                if (x - 50) % 100 == 0:
                    pygame.draw.rect(win, (40, 40, 40), (x, y, 50, 50))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    win.fill((10, 10, 10))
    draw_grid()

    pygame.display.flip()

    clock.tick(60)
