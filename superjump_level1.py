import pygame
from os.path import join
from component_loader import load_bullet_image, load_fruit_images, load_disappear_image, load_sounds, \
    load_end_arrow_image
from game_entities import Player, Block, Fire, Enemy, Fruit, DisappearAnimation
from superjump_level2 import run_level2

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

laser_sound, fruit_sound, player_hit, enemy_hit, potion_sound, jump_sound, game_over_sound, dead_sound, click_sound, hit_object_sound, level_transition_sound, level_finished = load_sounds()

enemy_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
disappear_group = pygame.sprite.Group()


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
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
    fruit_group.draw(window)
    for enemy in enemy_group:
        enemy.draw(window)
        enemy.draw_enemy_healthbar(window)
    disappear_group.draw(window)
    if total_score == 26:
        window.blit(arrow_img, (1150, 288))
        if player.rect.right > WIDTH:
            level_transition_sound.play()
            run_level2(window)
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
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, floor, player_health_bar):
    ratio = player_health_bar.hp / player_health_bar.max_hp
    filled_width = player_health_bar.w * ratio

    player.x_vel = 0
    collide_left = collide(player, objects, floor, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, floor, PLAYER_VEL * 2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, floor, player.y_vel)

    for obj in vertical_collide:
        if obj and obj.name == "fire":
            player.make_hit()
            hit_object_sound.play()
            player_health_bar.hp -= 8

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

    player_health_bar.draw_player_healthbar(window)


def run_level1(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Pink.png")
    block_size = 96

    player = Player(100, 100, 50, 50)

    fire1 = Fire(95, HEIGHT - block_size - 64, 16, 32)
    fire2 = Fire(505, HEIGHT - block_size - 64, 16, 32)
    fire1.on(), fire2.on()
    floor_objects = [Block(96, 128, i * block_size, HEIGHT - block_size, block_size) for i in
                     range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    floor = [*floor_objects]

    first_block = Block(96, 128, block_size * 2.55, HEIGHT - block_size * 6, block_size)
    last_block = Block(96, 128, block_size * 5.55, HEIGHT - block_size * 6, block_size)
    objects = [fire1, fire2, first_block, last_block, Block(96, 128, 0, HEIGHT - block_size * 2, block_size),
               Block(96, 128, block_size * 7.5, HEIGHT - block_size * 2, block_size),
               Block(96, 128, block_size * 12.55, HEIGHT - block_size * 4, block_size),
               Block(96, 128, block_size * 11.55, HEIGHT - block_size * 4, block_size),
               Block(96, 128, block_size * 10.55, HEIGHT - block_size * 4, block_size),
               Block(96, 128, block_size * 9.55, HEIGHT - block_size * 4, block_size),
               Block(96, 128, block_size * 4.55, HEIGHT - block_size * 6, block_size),
               Block(96, 128, block_size * 3.55, HEIGHT - block_size * 6, block_size),
               Block(96, 128, block_size * 1, HEIGHT - block_size * 7, block_size),
               Block(96, 128, block_size * 1, HEIGHT - block_size * 7,
                     block_size)]  # multiplying it by 2 bc the size encompasses both height and width. we want it to be more higher on the screen than the floor lvl

    if len(enemy_group) == 0:
        chicken1 = Enemy(WIDTH, 200, 651, 50, 50, 1.5, None, None, enemy_type="Chicken", sprite_width=32,
                         sprite_height=34)
        chicken2 = Enemy(WIDTH, 600, 651, 50, 50, 1.5, None, None, enemy_type="Chicken", sprite_width=32,
                         sprite_height=34)
        chicken3 = Enemy(WIDTH, 900, 618, 50, 50, 2.5, None, None, enemy_type="Chicken", sprite_width=32,
                         sprite_height=34)
        chicken4 = Enemy(WIDTH, 242, 173, 34, 44, 1.5, first_block, last_block, enemy_type="Chicken", sprite_width=32,
                         sprite_height=34)
        enemy_group.add(chicken1, chicken2, chicken3, chicken4)

    if len(fruit_group) == 0:
        cherry1 = Fruit(WIDTH, 170, 400, cherry_sheet, 1.5, 17)
        cherry2 = Fruit(WIDTH, 255, 500, cherry_sheet, 1.5, 17)
        cherry3 = Fruit(WIDTH, 325, 600, cherry_sheet, 1.5, 17)
        cherry4 = Fruit(WIDTH, 16, 280, cherry_sheet, 2, 17)
        kiwi1 = Fruit(WIDTH, 500, 400, kiwi_sheet, 1.5, 17)
        kiwi2 = Fruit(WIDTH, 500, 450, kiwi_sheet, 1.5, 17)
        kiwi3 = Fruit(WIDTH, 500, 500, kiwi_sheet, 1.5, 17)
        kiwi4 = Fruit(WIDTH, 500, 550, kiwi_sheet, 1.5, 17)
        orange1 = Fruit(WIDTH, 550, 180, orange_sheet, 1.5, 17)
        orange2 = Fruit(WIDTH, 360, 180, orange_sheet, 1.5, 17)
        orange3 = Fruit(WIDTH, 1008, 580, orange_sheet, 2.7, 17)
        strawberry1 = Fruit(WIDTH, 900, 350, strawberry_sheet, 1.5, 17)
        strawberry2 = Fruit(WIDTH, 900, 300, strawberry_sheet, 1.5, 17)
        strawberry3 = Fruit(WIDTH, 1083, 350, strawberry_sheet, 1.5, 17)
        strawberry4 = Fruit(WIDTH, 1083, 300, strawberry_sheet, 1.5, 17)
        strawberry5 = Fruit(WIDTH, 1159, 300, strawberry_sheet, 2.7, 17)
        fruit_group.add(cherry1, cherry2, cherry3, cherry4, kiwi1, kiwi2, kiwi3, kiwi4, orange1, orange2, orange3,
                        strawberry1, strawberry2, strawberry3, strawberry4, strawberry5)

    score = 0
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    jump_sound.play()
                    player.jump()

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

        for enemy in enemy_group:
            enemy.update_sprite(WIDTH)
        fruit_group.update(WIDTH)
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
                waiting_for_click = False
                enemy_group.empty()
                fruit_group.empty()
                disappear_group.empty()
                run_level1(window)
