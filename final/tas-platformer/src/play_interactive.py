import pygame

from game.game import GameState
from game.constants import INPUTS, SCANCODE_TO_NAME
from game.render import render_frame

pygame.init()
fpsClock = pygame.time.Clock()

# dog_sound = pygame.mixer.Sound("sounds/dog.mp3")
# pygame.mixer.music.load('sounds/dog.wav')
# pygame.mixer.music.play(-1)

game_state = GameState()
curr_inputs = 0
input_history = []
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN) and event.scancode in SCANCODE_TO_NAME:
            curr_inputs |= INPUTS[SCANCODE_TO_NAME[event.scancode]]

        if (event.type == pygame.KEYUP) and event.scancode in SCANCODE_TO_NAME:
            curr_inputs &= ~INPUTS[SCANCODE_TO_NAME[event.scancode]]

        if (event.type == pygame.KEYDOWN) and event.scancode not in SCANCODE_TO_NAME:
            print(event.scancode)

    # game_state.game_loop(inps[index])
    game_state.game_loop(curr_inputs)
    input_history.append(curr_inputs)
    render_frame(game_state)

    if not game_state.game_running:
        break

    # fpsClock.tick(1 / game_state._frame_time)
    fpsClock.tick(60)

pygame.quit()

if game_state.game_won:
    print("Game Won!")
else:
    print("Game Over!")

with open("moves", "w") as f:
    f.write("\n".join([str(x) for x in input_history]))
