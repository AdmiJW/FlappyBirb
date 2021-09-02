import random

import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C

from src.Pipe import Pipe

# Advanced Pipe - Inherits Pipe, but update() makes the pipe move vertically!?
class MovingPipe(Pipe):
    def __init__(self, screen: pygame.Surface, gap_top: int, left: int):
        super().__init__( screen, gap_top, left )
        self.gap_top = gap_top
        self.vertical_speed = random.choice( (-1, 1) ) * CONFIG.PIPE_MOVING_VERT_SPPED


    def update(self, dt):
        self._top_pipe_rect.left -= round(CONFIG.PIPE_SPEED * dt)
        self._bottom_pipe_rect.left -= round(CONFIG.PIPE_SPEED * dt)

        self._top_pipe_rect.top += round(self.vertical_speed * dt)
        self._bottom_pipe_rect.top += round(self.vertical_speed * dt)

        # Pipe is already at bottom
        if self._bottom_pipe_rect.top >= self._screen.get_height() - C.GROUND_HEIGHT:
            self.vertical_speed = -self.vertical_speed
            self._bottom_pipe_rect.top = self._screen.get_height() - C.GROUND_HEIGHT
            self._top_pipe_rect.bottom = self._bottom_pipe_rect.top - CONFIG.PIPE_GAP
        # Pipe is at top
        elif self._top_pipe_rect.bottom <= 0:
            self.vertical_speed = -self.vertical_speed
            self._top_pipe_rect.bottom = 0
            self._bottom_pipe_rect.top = CONFIG.PIPE_GAP
