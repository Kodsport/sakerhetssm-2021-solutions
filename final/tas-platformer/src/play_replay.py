import pygame
from pathlib import Path

from game.game import GameState
from game.constants import INPUTS, SCANCODE_TO_NAME
from game.render import render_frame

pygame.init()
fpsClock = pygame.time.Clock()

moves = [int(line) for line in Path("moves").read_text().split("\n")]

game_state = GameState()
curr_inputs = 0
input_history = []
running = True

for i, move in enumerate(moves):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()
    game_state.game_loop(move)
    input_history.append(curr_inputs)

    if not game_state.game_running:
        break

    print(i)
    if i > 0:
        render_frame(game_state)
        # fpsClock.tick(1 / game_state._frame_time)
        fpsClock.tick(100)


if game_state.game_won:
    print("Game Won!")
else:
    print("Game Over!")
