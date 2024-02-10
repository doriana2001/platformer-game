import pygame
from os.path import join
from component_loader import load_bullet_image, load_fruit_images, load_disappear_image, load_speed_potion_image, \
    load_sounds, load_spikes_image, load_spikehead_image, load_end_arrow_image
from game_entities import Player, Block, Fire, Enemy, Fruit, DisappearAnimation, SpeedPotion, Spikes

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
speed_potion_sheet = load_speed_potion_image()
spikes_sheet = load_spikes_image()
spikehead_sheet = load_spikehead_image()

laser_sound, fruit_sound, player_hit, enemy_hit, potion_sound, jump_sound, game_over_sound, dead_sound, click_sound, hit_object_sound, level_transition_sound, level_finished_sound = load_sounds()

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
    if total_score == 63:
        window.blit(arrow_img, (1086, 346))
        if player.rect.right > WIDTH:
            stage_completed(window)
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
    global PLAYER_VEL

    ratio = player_health_bar.hp / player_health_bar.max_hp
    filled_width = player_health_bar.w * ratio

    player.x_vel = 0
    collide_left = collide(player, objects, floor,
                           -PLAYER_VEL * 2)
    for obj in objects:
        if obj and obj.name == "spikes":
            if pygame.sprite.collide_rect(player, obj):
                player.make_hit()
                player_hit.play()
                player_health_bar.hp -= 1
                if filled_width + 137 <= 0:
                    print("Game Over!")
                    game_over(window)
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
            player_hit.play()
            player_health_bar.hp -= 12
            if filled_width + 137 <= 0:
                print("Game Over!")
                game_over(window)
        elif obj and (obj.x_coord == 272 and obj.y_coord == 0):
            if player.direction == "left":
                player.x_vel += 9
            elif player.direction == "right":
                player.x_vel -= 9

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
        if pygame.sprite.collide_rect(player, potion) and potion.name == "speed":
            potion_sound.play()
            PLAYER_VEL = 10
            potion.kill()

    player_health_bar.draw_player_healthbar(window)


def run_level3(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    block_size = 96

    player = Player(100, 100, 50, 50)
    fire1 = Fire(884, 218, 16, 32)
    fire2 = Fire(871, HEIGHT - block_size - 64, 16,
                 32)
    fire1.on(), fire2.on()
    floor_objects = [Block(272, 0, i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size,
                                                                                                   WIDTH * 2 // block_size)]
    floor = [*floor_objects]
    spikehead1 = Spikes(231, 580, spikehead_sheet)
    spikehead2 = Spikes(466, 580, spikehead_sheet)
    spikehead3 = Spikes(700, 580, spikehead_sheet)
    spikehead4 = Spikes(875, 290, spikehead_sheet)
    spikes_group.add(spikehead1, spikehead2, spikehead3, spikehead4)

    block1 = Block(272, 0, 950, HEIGHT - block_size * 4.4, block_size)
    block2 = Block(272, 0, 540, HEIGHT - block_size * 5.4, block_size)
    block3 = Block(272, 0, 445, HEIGHT - block_size * 5.4, block_size)
    block4 = Block(272, 0, 635, HEIGHT - block_size * 5.4, block_size)
    objects = [*spikes_group, block3, block1, block2, Block(272, 0, 335, HEIGHT - block_size * 4.4, block_size),
               Block(272, 0, 240, HEIGHT - block_size * 4.4, block_size),
               Block(272, 0, 815, HEIGHT - block_size * 4.4, block_size),
               Block(272, 0, 80, HEIGHT - block_size * 3.4, block_size),
               Block(272, 0, 1109, HEIGHT - block_size * 3.4, block_size),
               Block(272, 0, 1204, HEIGHT - block_size * 2.4, block_size)
               ]

    if len(enemy_group) == 0:
        slime1 = Enemy(WIDTH, 12, 656, 50, 50, 1.6, spikehead1, spikehead2, enemy_type="Slime", sprite_width=44,
                       sprite_height=30)
        slime2 = Enemy(WIDTH, 830, 598, 50, 50, 3.5, None, None, enemy_type="Slime", sprite_width=44,
                       sprite_height=30)
        bird1 = Enemy(WIDTH, 1000, 96, 80, 80, 1.6, block2, block3, enemy_type="BlueBird", sprite_width=32,
                      sprite_height=32)
        bird2 = Enemy(WIDTH, 694, 311, 80, 80, 3, block3, block4, enemy_type="BlueBird", sprite_width=32,
                      sprite_height=32)
        bird3 = Enemy(WIDTH, 100, 199, 80, 80, 2.3, block3, block4, enemy_type="BlueBird", sprite_width=32,
                      sprite_height=32)
        enemy_group.add(slime1, slime2, bird1, bird2, bird3)

    if len(fruit_group) == 0:
        melon1 = Fruit(WIDTH, 100, 400, melon_sheet, 1.8, 17)
        melon2 = Fruit(WIDTH, 515, 139, melon_sheet, 1.8, 17)
        melon3 = Fruit(WIDTH, 605, 515, melon_sheet, 3, 17)
        banana1 = Fruit(WIDTH, 432, 199, banana_sheet, 1.8, 17)
        banana2 = Fruit(WIDTH, 1106, 375, banana_sheet, 2.7, 17)
        banana3 = Fruit(WIDTH, 597, 199, banana_sheet, 1.8, 17)
        fruit_group.add(melon1, melon2, melon3, banana1, banana2, banana3)
    fast_potion = SpeedPotion(379, 530, speed_potion_sheet)
    potion_group.add(fast_potion)
    score = 43
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

        # Update enemy and fruit
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
                run_level3(window)


def stage_completed(window):
    level_finished_sound.play()
    pygame.display.update()

    title_font1 = pygame.font.SysFont("Retro Gaming", 100)
    window.fill((0, 0, 0))
    title_label1 = title_font1.render("STAGE 1 COMPLETED!", 1, (255, 255, 255))
    window.blit(title_label1, (WIDTH / 2 - title_label1.get_width() / 2, 300))

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
