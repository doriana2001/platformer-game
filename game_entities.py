import pygame
from os import listdir
from os.path import isfile, join
from healthbar import EnemyHealth, PlayerHealth
from component_loader import load_bullet_image, load_fruit_images, load_disappear_image, load_sounds

pygame.init()

WIDTH, HEIGHT = 1300, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

bullet_sheet = load_bullet_image()
cherry_sheet, kiwi_sheet, orange_sheet, apple_sheet, melon_sheet, pineapple_sheet, strawberry_sheet, banana_sheet = load_fruit_images()
disappear_img = load_disappear_image()

laser_sound, fruit_sound, player_hit, enemy_hit, potion_sound, jump_sound, game_over_sound, dead_sound, click_sound, hit_object_sound, level_transition_sound, level_finished_sound = load_sounds()

enemy_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
disappear_group = pygame.sprite.Group()


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False, scale=2):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            scaled_surface = pygame.transform.scale(surface, (int(width * scale), int(height * scale)))
            sprites.append(scaled_surface)

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size, x_coord, y_coord):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA,
                             32)
    rect = pygame.Rect(x_coord, y_coord, size,
                       size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32, True, scale=2)
    ANIMATION_DELAY = 6

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.enemy_score = 0
        self.hit = False
        self.hit_count = 0
        self.bullets = []
        self.cool_down_count = 0
        self.bullets_fired = 0
        self.burst_cooldown = 0
        self.h_width = 0
        self.h_height = 0
        # Health
        self.hitbox = (self.rect.x, self.rect.y, self.h_width, self.h_height)
        self.player_health_bar = PlayerHealth(15, 10, 50, 12, max_hp=100)

    def jump(self):

        self.y_vel = -self.GRAVITY * 9
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):

        self.hit = True
        self.hit_count = 0
        self.animation_state = "hit"

    def move_left(self, vel):

        if self.rect.x > 0:
            self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel

        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps, player_healthbar):

        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.player_health_bar.draw_player_healthbar(window)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 1.5:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):

        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):

        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):

        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        # default sprite sheet.
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(
            sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):

        self.update_sprite()
        win.blit(self.sprite, (self.rect.x, self.rect.y))

        for bullet in self.bullets:
            bullet.draw_bullet()

        self.player_health_bar.draw_player_healthbar(win)
        for enemy in enemy_group:
            enemy.draw_enemy_healthbar(window)

    def cooldown(self):

        if self.cool_down_count >= 35:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def shoot(self, objects, score, enemy_group):
        self.hit_by_bullet(objects, enemy_group, disappear_group)
        self.cooldown()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_f] and self.cool_down_count == 0:
            laser_sound.play()
            direction = 1 if self.direction == "right" else -1
            bullet = Bullet(self.rect.x, self.rect.y, self.direction)
            self.bullets.append(bullet)
            self.cool_down_count = 1

        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def hit_by_bullet(self, objects, enemy_group, disappear_group):
        for bullet in self.bullets:
            for enemy in enemy_group:
                if pygame.sprite.collide_mask(bullet, enemy):
                    enemy.make_hit()
                    enemy_hit.play()
                    if enemy.scale > 2:
                        enemy.enemy_health_bar.hp -= 4
                    else:
                        enemy.enemy_health_bar.hp -= 7
                    if enemy.enemy_health_bar.hp <= 0:
                        dead_sound.play()
                        enemy_group.remove(enemy)
                        disappear = DisappearAnimation(WIDTH, enemy.rect.x - 5, enemy.rect.y, disappear_img,
                                                       3 if enemy.scale > 1.5 else 1.2, 6)
                        self.enemy_score += 2 if enemy.scale > 1.5 else 1
                        disappear_group.add(disappear)
                    self.bullets.remove(bullet)
                    break
        for bullet in self.bullets:
            for obj in objects:
                if pygame.sprite.collide_mask(bullet, obj):
                    self.bullets.remove(bullet)


class Enemy(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SPRITES = load_sprite_sheets("Enemy", "Chicken", 32, 34, True, scale=1.7)
    ANIMATION_DELAY = 5

    def __init__(self, WIDTH, x, y, width, height, scale=1.4, target_object=None, target_object2=None, enemy_type=None,
                 sprite_width=None, sprite_height=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.enemy_type = enemy_type
        self.sprite_width = sprite_width
        self.scale = scale
        self.sprite_height = sprite_height
        self.SPRITES = load_sprite_sheets("Enemy", self.enemy_type, self.sprite_width, self.sprite_height, True,
                                          scale=self.scale)
        self.direction = 1
        self.animation_count = 0
        self.target_object = target_object
        self.target_object2 = target_object2
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.direction_text = ""
        self.enemy_health_bar = EnemyHealth(self.rect.x, self.rect.y, 50, 12, max_hp=20)

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move(self, x_vel):
        self.rect.x += x_vel

    def loop(self, fps):
        self.x_vel = 1 * self.direction
        self.move(self.x_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:  # 2 seconds
            self.hit = False
            self.hit_count = 0
        self.rect.x += self.x_vel
        self.fall_count += 1
        self.update_sprite(WIDTH)

    def update_sprite(self, WIDTH):
        sprite_sheet = "run"
        if self.hit:
            sprite_sheet = "hit"

        if self.direction == 1:
            self.direction_text = "left"
        elif self.direction == -1:
            self.direction_text = "right"

        sprite_sheet_name = sprite_sheet + "_" + self.direction_text
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(
            sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def collide(self, objects):
        collided_objects = []

        for obj in objects:
            if self.rect.colliderect(obj.rect):
                collided_objects.append(obj)

        return collided_objects

    def handle_move(self, objects):
        if self.target_object != None or self.target_object2 != None:
            if (self.direction == 1 and self.rect.right >= self.target_object2.rect.right) or \
                    (self.direction == -1 and self.rect.left <= self.target_object.rect.left):
                if self.rect.bottom == self.target_object.rect.top or self.rect.bottom == self.target_object2.rect.top:
                    self.direction *= -1

        horizontal_collide = self.collide(objects)
        if self.rect.right > WIDTH:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1

        for obj in horizontal_collide:
            if obj:
                self.direction *= -1

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        self.update_sprite(WIDTH)
        win.blit(self.sprite, (self.rect.x, self.rect.y))

    def draw_enemy_healthbar(self, win):
        self.enemy_health_bar.x = self.rect.x + 6
        self.enemy_health_bar.y = self.rect.y - 14
        self.enemy_health_bar.draw_enemy_healthbar(win)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, WIDTH, x, y, sprite_sheet, scale, animation_steps=None):
        super().__init__()

        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.scale = scale

        self.animation_steps = animation_steps
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, WIDTH):
        ANIMATION_COOLDOWN = 35
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def get_position(self):
        return self.rect.x, self.rect.y


class DisappearAnimation(pygame.sprite.Sprite):
    def __init__(self, WIDTH, x, y, sprite_sheet, scale, animation_steps=None):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.scale = scale

        self.animation_steps = animation_steps
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, WIDTH):
        ANIMATION_COOLDOWN = 35
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.kill()


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 20
        self.y = y + 41
        self.direction = direction
        self.image = bullet_sheet
        self.rect = pygame.Rect(self.x, self.y, 35, 35)
        self.mask = pygame.mask.from_surface(self.image)

    def draw_bullet(self):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        if self.direction == "right":
            self.x += 15
        elif self.direction == "left":
            self.x -= 15
        self.rect.x = self.x
        self.mask = pygame.mask.from_surface(self.image)

    def off_screen(self):
        return not (self.x >= 0 and self.x <= WIDTH)


class Object(
    pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Block(Object):
    def __init__(self, x_coord, y_coord, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size, x_coord,
                          y_coord)
        self.image.blit(block, (0, 0))
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.x = x
        self.y = y
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0


class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name="health"):
        super().__init__()
        width, height = image.get_size()
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(image)
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class SpeedPotion(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name="speed"):
        super().__init__()
        width, height = image.get_size()
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(image)
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name="spikes"):
        super().__init__()
        width, height = image.get_size()
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(image)
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
