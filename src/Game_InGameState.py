import pygame

import src.CONSTANT as C

from src.Bird import Bird
from src.PipeSystem import PipeSystem

import src.Audio as Audio

import src.QuitState as QuitState
import src.Game_DyingState as Game_DyingState
import src.Game_PausedState as Game_PausedState


class Game_InGame:
    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, bird: Bird, pipe_system: PipeSystem ):
        self._screen = screen
        self._clock = clock
        self._bird = bird
        self._pipe_system = pipe_system
        self._next_state = self


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = QuitState.Quit()
            elif event.type == pygame.KEYDOWN:
                # Jumps
                if event.key == pygame.K_SPACE:
                    self._bird.jump()
                    Audio.play_jump_sfx()
                # Pause
                elif event.key == pygame.K_RETURN:
                    self._next_state = Game_PausedState.Game_Paused(self._screen, self._clock,
                                                                    self._bird, self._pipe_system )
                    Audio.play_selected_sfx()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._bird.jump()
                Audio.play_jump_sfx()


    # Checks for collision between the bird and pipe or ground/sky. If collision is done, next state is dying
    # Also, we need to check for scoring
    def update(self, dt):
        self._bird.update(dt)
        self._pipe_system.update(dt)

        # Check collision between bird and ground/sky/pipes. Will go dying if collision detected
        if self._bird.rect.bottom >= self._screen.get_height() - C.GROUND_HEIGHT or self._bird.rect.top < -50\
                or self._pipe_system.is_collide( self._bird.rect):
            self._next_state = Game_DyingState.Game_Dying(self._screen, self._clock, self._bird, self._pipe_system)
            Audio.play_collision_sfx()


    def render(self):
        self._bird.render()
        self._pipe_system.render()

    def get_next_state(self):
        return self._next_state
