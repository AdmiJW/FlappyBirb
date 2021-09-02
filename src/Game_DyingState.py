import pygame

from src.Bird import Bird
from src.PipeSystem import PipeSystem

import src.QuitState as QuitState

class Game_Dying:
    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, bird: Bird, pipe_system: PipeSystem):
        self._screen = screen
        self._clock = clock
        self._bird = bird
        self._pipe_system = pipe_system
        self._next_state = self

        # Make the bird jump before falling
        self._bird.jump()


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = QuitState.Quit()

    def update(self, dt):
        self._bird.update(dt)

        if self._bird.centery > self._screen.get_height() + 50:
            self._next_state = None

    def render(self):
        self._bird.render()
        self._pipe_system.render()


    def get_next_state(self):
        return self._next_state
