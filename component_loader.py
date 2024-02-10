import pygame
import os
from spritesheet_module import SpriteSheet


def load_fireball_image():
    fireball_img = pygame.image.load("assets/Bullets/Firestrike.png").convert_alpha()
    return SpriteSheet(fireball_img)


def load_spikes_image():
    spikes_img = pygame.transform.scale2x(pygame.image.load("assets/Traps/Spikes/Idle.png").convert_alpha())
    return spikes_img


def load_end_arrow_image():
    end_arrow_img = pygame.transform.scale2x(pygame.image.load("assets/Items/Checkpoints/arrow.png").convert_alpha())
    return end_arrow_img


def load_bullet_image():
    bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("assets/Bullets/light_bullet.png")), (22, 11))
    return bullet_img


def load_spikehead_image():
    spikehead_image = pygame.transform.scale(pygame.image.load(os.path.join("assets/Traps/Spike Head/idle.png")),
                                             (111, 111))
    return spikehead_image


def load_health_potion_image():
    health_potion = pygame.transform.scale(
        pygame.image.load(os.path.join("assets/HeartHealthBar", "health_potion.png")), (58, 58))
    return health_potion


def load_speed_potion_image():
    speed_potion = pygame.transform.scale(pygame.image.load(os.path.join("assets/Items/Potions", "speed_potion.png")),
                                          (58, 58))
    return speed_potion


def load_fruit_images():
    cherry_sheet_img = pygame.image.load("assets/Fruits/Cherries.png").convert_alpha()
    kiwi_sheet_img = pygame.image.load("assets/Fruits/Kiwi.png").convert_alpha()
    orange_sheet_img = pygame.image.load("assets/Fruits/Orange.png").convert_alpha()
    apple_sheet_img = pygame.image.load("assets/Fruits/Apple.png").convert_alpha()
    melon_sheet_img = pygame.image.load("assets/Fruits/Melon.png").convert_alpha()
    pineapple_sheet_img = pygame.image.load("assets/Fruits/Pineapple.png").convert_alpha()
    strawberry_sheet_img = pygame.image.load("assets/Fruits/Strawberry.png").convert_alpha()
    banana_sheet_img = pygame.image.load("assets/Fruits/Bananas.png").convert_alpha()

    cherry_sheet = SpriteSheet(cherry_sheet_img)
    kiwi_sheet = SpriteSheet(kiwi_sheet_img)
    orange_sheet = SpriteSheet(orange_sheet_img)
    apple_sheet = SpriteSheet(apple_sheet_img)
    melon_sheet = SpriteSheet(melon_sheet_img)
    pineapple_sheet = SpriteSheet(pineapple_sheet_img)
    strawberry_sheet = SpriteSheet(strawberry_sheet_img)
    banana_sheet = SpriteSheet(banana_sheet_img)

    return cherry_sheet, kiwi_sheet, orange_sheet, apple_sheet, melon_sheet, pineapple_sheet, strawberry_sheet, banana_sheet


def load_disappear_image():
    disappear_img_animation = pygame.image.load("assets/Fruits/Collected.png").convert_alpha()
    return SpriteSheet(disappear_img_animation)


def load_sounds():
    laser_sound = pygame.mixer.Sound("assets/Sounds/shoot.wav")
    fruit_sound = pygame.mixer.Sound("assets/Sounds/fruit_collect.wav")
    player_hit = pygame.mixer.Sound("assets/Sounds/hit_damage.wav")
    enemy_hit = pygame.mixer.Sound("assets/Sounds/boss_hit.wav")
    potion_sound = pygame.mixer.Sound("assets/Sounds/potion_collect.wav")
    jump_sound = pygame.mixer.Sound("assets/Sounds/jump.wav")
    game_over_sound = pygame.mixer.Sound("assets/Sounds/game_over.wav")
    dead_sound = pygame.mixer.Sound("assets/Sounds/dead_sound.wav")
    click_sound = pygame.mixer.Sound("assets/Sounds/click_sound.wav")
    hit_object_sound = pygame.mixer.Sound("assets/Sounds/hit_by_object.wav")
    level_transition_sound = pygame.mixer.Sound("assets/Sounds/level_transition.wav")
    level_finished_sound = pygame.mixer.Sound("assets/Sounds/level_finished.wav")
    return laser_sound, fruit_sound, player_hit, enemy_hit, potion_sound, jump_sound, game_over_sound, dead_sound, click_sound, hit_object_sound, level_transition_sound, level_finished_sound
