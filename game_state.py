import pygame
from superjump_level1 import run_level1
from superjump_level2 import run_level2
from superjump_level3 import run_level3

WIDTH, HEIGHT = 1300, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0


def main():
    run_level1(window)
    run_level2(window)
    run_level3(window)


if __name__ == "__main__":
    main()
