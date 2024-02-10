import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))


class PlayerHealth():
    empty_bar_png = pygame.image.load("assets/HeartHealthBar/health_bar_decorator.png")
    empty_bar = pygame.transform.scale(empty_bar_png, (244, 62)).convert_alpha()

    filled_bar_png = pygame.image.load("assets/HeartHealthBar/health_bar_filled.png")
    filled_bar = pygame.transform.scale(filled_bar_png, (244, 62)).convert_alpha()

    pixel_heart_png = pygame.image.load("assets/HeartHealthBar/pixel_heart.png")
    pixel_heart = pygame.transform.scale(pixel_heart_png, (244, 62)).convert_alpha()

    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw_player_healthbar(self, win):
        ratio = self.hp / self.max_hp

        win.blit(PlayerHealth.empty_bar, (self.x, self.y - 5))
        filled_width = self.w * ratio
        filled_rect = pygame.Rect(self.x, self.y, filled_width + 137, self.h + 80)
        win.blit(PlayerHealth.filled_bar, (self.x + 52, self.y + 5), filled_rect)
        win.blit(PlayerHealth.pixel_heart, (self.x + 1, self.y - 5))


class EnemyHealth():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw_enemy_healthbar(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (200, 41, 32), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, (50, 205, 50), (self.x, self.y, self.w * ratio, self.h))
