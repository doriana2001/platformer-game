import pygame
import sys
from game_state import main

pygame.init()

WIDTH, HEIGHT = 1300, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Start Menu")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

button_click = pygame.mixer.Sound("assets/Sounds/menu_click.wav")
button_hover = pygame.mixer.Sound("assets/Sounds/hover_sound.wav")
startup_sound = pygame.mixer.Sound("assets/Sounds/startup_menu.wav")

button_width, button_height = 388, 122
button_img = pygame.image.load("assets/StartButton/normal.png").convert_alpha()
normal_button_img = pygame.transform.scale(button_img, (button_width * 2, button_height * 2)).convert_alpha()
hover_img = pygame.image.load("assets/StartButton/hover.png").convert_alpha()
hover_button_img = pygame.transform.scale(hover_img, (button_width * 2, button_height * 2)).convert_alpha()
clicked_img = pygame.image.load("assets/StartButton/clicked.png").convert_alpha()
clicked_button_img = pygame.transform.scale(clicked_img, (button_width * 2, button_height * 2)).convert_alpha()

font_size = 153
platformer_jump_font_size = 100
font = pygame.font.SysFont("RetroGaming", font_size)
platformer_jump_font = pygame.font.SysFont("RetroGaming", platformer_jump_font_size)

normal_text_color = BLACK
hover_text_color = GRAY


class Button:
    def __init__(self, x, y, width, height, normal_img, hover_img, clicked_img, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_img = normal_img
        self.hover_img = hover_img
        self.clicked_img = clicked_img
        self.text = text
        self.image = self.normal_img
        self.text_color = normal_text_color

    def draw(self):
        window.blit(self.image, self.rect)
        if self.text and self.image is not self.clicked_img:
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 10))
            window.blit(text_surface, text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


def draw_platformer_jump():
    text_surface = platformer_jump_font.render("Platformer Jump", True, RED)
    shadow_surface = platformer_jump_font.render("Platformer Jump", True, BLACK)

    shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 2, button_y - 300 + 2))
    window.blit(shadow_surface, shadow_rect)

    text_rect = text_surface.get_rect(center=(WIDTH // 2, button_y - 300))
    window.blit(text_surface, text_rect)


button_x, button_y = (WIDTH - button_width * 2) // 2, (HEIGHT - button_height * 2) // 2 + 160
button_text = "START"
button = Button(button_x, button_y - 100, button_width * 2, button_height * 2, normal_button_img, hover_button_img,
                clicked_button_img, button_text)
startup_sound.play()
button_hover_played = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if button.is_hovered():
                button.image = button.hover_img
                button.text_color = hover_text_color
            else:
                button.image = button.normal_img
                button.text_color = normal_text_color

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_hovered():
                button.image = button.clicked_img
                button_click.play()
                main()
        elif event.type == pygame.MOUSEBUTTONUP:
            if button.is_hovered():
                print("Button clicked!")
                running = False

    picture = pygame.image.load("assets/StartBackground/menu_bg.jpg")
    picture = pygame.transform.scale(picture, (1300, 800))
    window.blit(picture, (0, 0))

    button.draw()
    draw_platformer_jump()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
