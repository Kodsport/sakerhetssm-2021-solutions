from game.game_board import Floor, Wall, Door
import pygame

from game.game import GameState
from game.constants import INPUTS, SCANCODE_TO_NAME
from game.render import render_frame, inverse_transform_pos
import numpy as np
from game.utils import Rect, Vec2

pygame.init()
fpsClock = pygame.time.Clock()

# dog_sound = pygame.mixer.Sound("sounds/dog.mp3")
# pygame.mixer.music.load('sounds/dog.wav')
# pygame.mixer.music.play(-1)

game_state = GameState()


def save_level():
    level_code = "from .game_board import Wall, Floor, Door\n"
    level_code += "walls = [\n"
    for wall in game_state.board.walls:
        level_code += (
            "Wall([{:.2f},{:.2f}],{:.2f}),".format(
                wall.position.x, wall.position.y, wall.height
            )
            + "\n"
        )
    level_code += "]\n"
    level_code += "floors = [\n"
    for floor in game_state.board.floors:
        level_code += (
            "Floor([{:.2f},{:.2f}],{:.2f}),".format(
                floor.position.x, floor.position.y, floor.width
            )
            + "\n"
        )
    level_code += "]\n"
    open("game/level.py", "w").write(level_code)


curr_inputs = 0
running = True
short = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.scancode == 225:
            short = True

        if event.type == pygame.KEYUP and event.scancode == 225:
            short = False

        if (event.type == pygame.KEYDOWN) and event.scancode in SCANCODE_TO_NAME:
            curr_inputs |= INPUTS[SCANCODE_TO_NAME[event.scancode]]

        if (event.type == pygame.KEYUP) and event.scancode in SCANCODE_TO_NAME:
            curr_inputs &= ~INPUTS[SCANCODE_TO_NAME[event.scancode]]

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = inverse_transform_pos(
                event.pos[0], event.pos[1], game_state.player.center
            )
            click_pos = (round(click_pos[0] * 10) / 10, round(click_pos[1] * 10) / 10)
            if event.button == 2:
                for wall in game_state.board.walls:
                    if np.linalg.norm(wall.position - Vec2(click_pos)) < 0.2:
                        game_state.board.walls.remove(wall)
                        break
                for floor in game_state.board.floors:
                    if np.linalg.norm(floor.position - Vec2(click_pos)) < 0.2:
                        game_state.board.floors.remove(floor)
                        break
            if event.button == 1:
                if short:
                    game_state.board.floors.append(Floor(click_pos, width=0.5))
                else:
                    game_state.board.floors.append(Floor(click_pos))
                # print("Floor([{},{}])".format(click_pos[0], click_pos[1]))
            if event.button == 3:
                if short:
                    game_state.board.walls.append(Wall(click_pos, height=0.5))
                else:
                    game_state.board.walls.append(Wall(click_pos))

            save_level()

    if curr_inputs & INPUTS["A"]:
        game_state.player.position.x -= 0.05
    if curr_inputs & INPUTS["S"]:
        game_state.player.position.y -= 0.05
    if curr_inputs & INPUTS["W"]:
        game_state.player.position.y += 0.05
    if curr_inputs & INPUTS["D"]:
        game_state.player.position.x += 0.05
    # game_state.game_loop(curr_inputs)
    render_frame(game_state)
    fpsClock.tick(1 / game_state._frame_time)


pygame.quit()
