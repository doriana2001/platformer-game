import pygame
from os.path import join
from component_loader import load_bullet_image, load_fruit_images, load_disappear_image, load_health_potion_image, \
    load_sounds, load_spikes_image, load_end_arrow_image
from game_entities import Player, Block, Fire, Enemy, Fruit, DisappearAnimation, HealthPotion, Spikes
from superjump_level3 import run_level3

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Platformer Jump")

WIDTH, HEIGHT = 1300, 800
FPS = 60
PLAYER_VEL = 6

window = pygame.display.set_mode((WIDTH, HEIGHT))

bullet_sheet = load_bullet_image()
cherry_sheet, kiwi_sheet, orange_sheet, apple_sheet, melon_sheet, pineapple_sheet, strawberry_sheet, banana_sheet = load_fruit_images()
disappear_img = load_disappear_image()
arrow_img = load_end_arrow_image()
health_potion_sheet = load_health_potion_image()
spikes_sheet = load_spikes_image()

laser_sound, fruit_sound, player_hit, enemy_hit, potion_sound, jump_sound, game_over_sound, dead_sound, click_sound, hit_object_sound, level_transition_sound, level_finished = load_sounds()

enemy_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
disappear_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(
            WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image


def draw(window, background, bg_image, player, objects, floor, score):
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window)
    for tile in floor:
        tile.draw(window)
    score2 = player.hit_by_bullet(objects, enemy_group, disappear_group)
    score_font = pygame.font.SysFont("Retro Gaming", 50)
    total_score = score + player.enemy_score
    score_label = score_font.render(f"Score: {total_score}", 1, (255, 255, 255))
    window.blit(score_label, (987, 5))
    player.draw(window)

    for bullet in player.bullets:
        bullet.draw_bullet()
    potion_group.draw(window)
    fruit_group.draw(window)
    for enemy in enemy_group:
        enemy.draw(window)
        enemy.draw_enemy_healthbar(window)
    disappear_group.draw(window)
    if total_score == 43:
        window.blit(arrow_img, (1150, 346))
        if player.rect.right > WIDTH:
            level_transition_sound.play()
            run_level3(window)
    elif player.rect.right > WIDTH:
        player.rect.right = WIDTH
    pygame.display.update()


def handle_vertical_collision(player, objects, floor, dy):
    collided_objects = []
    all_objects = objects + floor
    for obj in all_objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)
    if player.rect.top < 0:
        player.hit_head()
        player.rect.top = 0
    return collided_objects


def collide(player, objects, floor, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    all_objects = objects + floor
    for obj in all_objects:
        if pygame.sprite.collide_mask(player,
                                      obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, floor,
                player_health_bar):
    ratio = player_health_bar.hp / player_health_bar.max_hp
    filled_width = player_health_bar.w * ratio

    player.x_vel = 0
    collide_left = collide(player, objects, floor,
                           -PLAYER_VEL * 2)
    collide_right = collide(player, objects, floor, PLAYER_VEL * 2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, floor,
                                                 player.y_vel)
    for obj in vertical_collide:
        if obj and (obj.name == "fire" or obj.name == "spikes"):
            player.make_hit()
            hit_object_sound.play()
            player_health_bar.hp -= 12
            if filled_width + 137 <= 0:
                print("Game Over!")
                game_over(window)

    for enemy in enemy_group:
        if pygame.sprite.collide_mask(player, enemy):
            if filled_width + 137 <= 0:
                print("Game Over!")
                game_over(window)
            player.make_hit()
            player_hit.play()
            if enemy.scale < 2:
                player_health_bar.hp -= 1
            else:
                player_health_bar.hp -= 3

    for potion in potion_group:
        if pygame.sprite.collide_rect(player,
                                      potion) and potion.name == "health" and player_health_bar.hp < player_health_bar.max_hp:
            potion_sound.play()
            potion.kill()
            health_to_restore = min(player_health_bar.max_hp - player_health_bar.hp, 35)
            player_health_bar.hp += health_to_restore
        elif pygame.sprite.collide_rect(player, potion) and player_health_bar.hp == player_health_bar.max_hp:
            potion_sound.play()
            potion.kill()

    player_health_bar.draw_player_healthbar(window)


def run_level2(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")
    block_size = 96
    player = Player(100, 100, 50, 50)
    fire1 = Fire(884, 218, 16, 32)
    fire2 = Fire(871, HEIGHT - block_size - 64, 16,
                 32)
    fire1.on(), fire2.on()
    floor_objects = [Block(0, 128, i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size,
                                                                                                   WIDTH * 2 // block_size)]
    floor = [*floor_objects]

    spikes1 = Spikes(1060, 440, spikes_sheet)
    spikes2 = Spikes(1095, 440, spikes_sheet)
    spikes3 = Spikes(1130, 440, spikes_sheet)
    spikes4 = Spikes(1195, 440, spikes_sheet)
    spikes_group.add(spikes1, spikes2, spikes3, spikes4)

    block1 = Block(0, 128, 570, HEIGHT - block_size * 6.4, block_size)
    block2 = Block(0, 128, 750, HEIGHT - block_size * 6.4, block_size)
    block3 = Block(0, 128, 945, HEIGHT - block_size * 4.4, block_size)
    objects = [fire1, fire2, *spikes_group, Block(0, 128, 300, HEIGHT - block_size * 3, block_size),
               Block(0, 128, 480, HEIGHT - block_size * 4.3, block_size),
               Block(0, 128, 370, HEIGHT - block_size * 6.4, block_size),
               Block(0, 128, 180, HEIGHT - block_size * 6.4, block_size),
               block3, block1, block2, Block(0, 128, 660, HEIGHT - block_size * 6.4, block_size),
               Block(0, 128, 850, HEIGHT - block_size * 5.4, block_size),
               Block(0, 128, 1039, HEIGHT - block_size * 3.4, block_size),
               Block(0, 128, 1134, HEIGHT - block_size * 3.4, block_size),
               Block(0, 128, 1230, HEIGHT - block_size * 3.4, block_size)
               ]

    if len(enemy_group) == 0:
        bunny1 = Enemy(WIDTH, 200, 634, 50, 50, 1.6, None, None, enemy_type="Bunny", sprite_width=34,
                       sprite_height=44)
        bunny2 = Enemy(WIDTH, 600, 594, 50, 50, 2.5, None, None, enemy_type="Bunny", sprite_width=34,
                       sprite_height=44)
        turtle1 = Enemy(WIDTH, 974, 336, 80, 80, 1.6, block2, block3, enemy_type="Turtle", sprite_width=44,
                        sprite_height=26)
        turtle2 = Enemy(WIDTH, 610, 126, 80, 80, 2.3, block1, block2, enemy_type="Turtle", sprite_width=44,
                        sprite_height=26)
        enemy_group.add(bunny1, bunny2, turtle1, turtle2)

    if len(fruit_group) == 0:
        apple1 = Fruit(WIDTH, 316, 440, apple_sheet, 1.8, 17)
        apple2 = Fruit(WIDTH, 498, 322, apple_sheet, 1.8, 17)
        apple3 = Fruit(WIDTH, 715, 110, apple_sheet, 2.6, 17)
        pineapple1 = Fruit(WIDTH, 384, 123, pineapple_sheet, 1.8, 17)
        pineapple2 = Fruit(WIDTH, 1135, 323, pineapple_sheet, 2.7, 17)
        fruit_group.add(apple1, apple2, apple3, pineapple1, pineapple2)
    hp_potion = HealthPotion(586, 124, health_potion_sheet)
    potion_group.add(hp_potion)
    score = 26
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                    jump_sound.play()

        for fruit in fruit_group:
            if pygame.sprite.collide_rect(player, fruit):
                fruit.kill()
                fruit_sound.play()
                x_position, y_position = fruit.rect.x, fruit.rect.y
                if fruit.scale < 2.5:
                    scale = 1.5
                elif fruit.scale == 2:
                    scale = 2.4
                else:
                    x_position -= 7
                    y_position -= 5
                    scale = 3.3
                disappear = DisappearAnimation(WIDTH, x_position, y_position, disappear_img, scale, 6)
                score += 3 if fruit.scale >= 2.5 else 2 if fruit.scale == 2 else 1
                disappear_group.add(disappear)

        potion_group.update(WIDTH)
        for enemy in enemy_group:
            enemy.update_sprite(WIDTH)
        fruit_group.update(WIDTH)
        spikes_group.update(WIDTH)
        disappear_group.update(WIDTH)

        player.loop(FPS, player.player_health_bar)
        for enemy in enemy_group:
            enemy.loop(FPS)
        fire1.loop()
        fire2.loop()

        handle_move(player, objects, floor, player.player_health_bar)

        draw(window, background, bg_image, player, objects, floor, score)

        for enemy in enemy_group:
            enemy.handle_move(objects)
        player.shoot(objects, score, enemy_group)

        pygame.display.update()

    pygame.quit()
    quit()


def game_over(window):
    game_over_sound.play()
    pygame.display.update()

    title_font1 = pygame.font.SysFont("Retro Gaming", 100)
    title_font2 = pygame.font.SysFont("comicsans", 24)
    window.fill((0, 0, 0))
    title_label1 = title_font1.render("GAME OVER!", 1, (255, 0, 0))
    title_label2 = title_font2.render("Click on screen to restart", 1, (255, 255, 255))
    window.blit(title_label1, (WIDTH / 2 - title_label1.get_width() / 2, 300))
    window.blit(title_label2, (WIDTH / 2 - title_label1.get_width() / 2 + 207, 450))

    pygame.display.update()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                waiting_for_click = False
                enemy_group.empty()
                fruit_group.empty()
                disappear_group.empty()
                potion_group.empty()
                run_level2(window)
