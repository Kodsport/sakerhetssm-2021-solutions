import pygame
import numpy as np

from .game_board import Floor, Wall, Door
from .game import Player
from .boss import Boss

# Init screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

scale_factor = 100
player_offset_x = screen_width / 2
player_offset_y = screen_height / 2
player_width = int(0.4 * scale_factor)
player_height = scale_factor

player_img = pygame.image.load("images/dog.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_width, player_height))

player_img_left = pygame.image.load("images/left.png").convert_alpha()
player_img_left = pygame.transform.scale(player_img_left, (player_width, player_height))

player_img_right = pygame.image.load("images/right.png").convert_alpha()
player_img_right = pygame.transform.scale(
    player_img_right, (player_width, player_height)
)

floor_img = pygame.image.load("images/block.png")
wall_img = pygame.image.load("images/block.png")

door_img = pygame.image.load("images/door.png")
door_img = pygame.transform.scale(
    pygame.transform.rotate(door_img, 90),
    (int(0.1 * scale_factor), int(1.5 * scale_factor)),
)

boss_img = pygame.image.load("images/boss.png").convert_alpha()
boss_img = pygame.transform.scale(
    boss_img,
    (int(scale_factor), int(3 * scale_factor)),
)

pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 30)


def transform_pos(x, y, player_pos):
    return (
        (x * scale_factor - player_pos[0] * scale_factor) + player_offset_x,
        (-y * scale_factor + player_pos[1] * scale_factor) + player_offset_y,
    )


def inverse_transform_pos(x, y, player_pos):
    return (
        (x - player_offset_x) / scale_factor + player_pos[0],
        -((y - player_offset_y) / scale_factor - player_pos[1]),
    )


def draw_bar(pos, width, part, color1, color2):
    pygame.draw.rect(screen, color1, (pos[0], pos[1], width, 10))
    pygame.draw.rect(
        screen,
        color2,
        (
            pos[0],
            pos[1],
            (min(part, 1)) * width,
            10,
        ),
    )


def render_frame(game_state):
    screen.fill((255, 255, 255))

    player_pos = game_state.player.center

    for wall in game_state.board.walls:
        pos = wall.position
        screen.blit(
            pygame.transform.scale(
                pygame.transform.rotate(wall_img, 90),
                (int(0.1 * scale_factor), int(wall.height * scale_factor)),
            ),
            transform_pos(pos[0], pos[1] + wall.height, player_pos),
        )

    for floor in game_state.board.floors:
        pos = floor.position
        screen.blit(
            pygame.transform.scale(
                floor_img, (int(floor.width * scale_factor), int(scale_factor * 0.1))
            ),
            transform_pos(pos[0], pos[1], player_pos),
        )

    for door in game_state.board.doors:
        if not door.open:
            pos = door.position
            screen.blit(door_img, transform_pos(pos[0], pos[1] + 1.5, player_pos))

    for button in game_state.board.buttons:
        pos = button.position
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            transform_pos(pos[0], pos[1], player_pos),
            20,
            3 if button.is_pressed else 0,
        )

        if np.linalg.norm(pos - player_pos) < 0.3:
            txt = myfont.render("B to press button", True, (0, 0, 0))
            screen.blit(txt, (screen_width - 300, 10))

    # Draw boss
    pos = game_state.boss.position
    img = boss_img
    screen.blit(img, transform_pos(pos[0], pos[1] + 3, player_pos))
    health_pos = transform_pos(pos[0] + 0.1, pos[1] + 3, player_pos)
    draw_bar(health_pos, 60, game_state.boss.health / 100, (255, 0, 0), (0, 255, 0))

    # Draw player
    pos = game_state.player.position
    img = player_img
    if game_state.player.velocity.x < -0.001:
        img = player_img_left
    if game_state.player.velocity.x > 0.001:
        img = player_img_right
    screen.blit(img, transform_pos(pos[0], pos[1] + 1, player_pos))
    if game_state.player.can_attack:
        health_pos = transform_pos(pos[0] - 0.05, pos[1] + 1.2, player_pos)
        kooldown_pos = transform_pos(pos[0] - 0.05, pos[1] + 1.5, player_pos)
        draw_bar(
            health_pos, 50, game_state.player.health / 50, (255, 0, 0), (0, 255, 0)
        )
        draw_bar(
            kooldown_pos,
            50,
            game_state.player.time_since_last_attack
            / game_state.player.ATTACK_KOOLDOWN,
            (255, 255, 255),
            (0, 0, 255),
        )

    # screen.blit(floor_img, (200-player_pos[0], 300-player_pos[1]))
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    pygame.display.flip()
