import random

import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C

import src.Audio as Audio

from src.Pipe import Pipe
from src.MovingPipe import MovingPipe


class PipeSystem(pygame.sprite.Group):
    # When initializes, will generate as many pipes at the right edge of the screen (not visible)
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self.prev_gap_top = self._screen.get_height() // 2
        self.pipe_stack = []
        self.score = 0

        # Generate an initial pipe at the right edge of the screen.
        self.generate_new_pipe()

    # Generates and updates the gap top for a new pipe
    def generate_gap_top(self):
        # Adjusts the prev gap top
        self.prev_gap_top = max(CONFIG.PIPE_DIFFERENCE, self.prev_gap_top)
        self.prev_gap_top = min(self._screen.get_height() - C.GROUND_HEIGHT - CONFIG.PIPE_DIFFERENCE - CONFIG.PIPE_GAP,
                                self.prev_gap_top)
        self.prev_gap_top = random.randrange(self.prev_gap_top - CONFIG.PIPE_DIFFERENCE,
                                             self.prev_gap_top + CONFIG.PIPE_DIFFERENCE + 1)
        return self.prev_gap_top

    # Generates a new pipe and push it to self.pipe_stack at the back
    # 50% chance of a moving pipe instead of regular pipe on score 15 onwards
    def generate_new_pipe(self):
        if self.score < CONFIG.MOVING_PIPE_MIN_SCORE:
            self.pipe_stack.append(Pipe(self._screen, self.generate_gap_top(), self._screen.get_width()))
        else:
            pipe_class = random.choices((Pipe, MovingPipe), (1 - CONFIG.MOVING_PIPE_CHANCE, CONFIG.MOVING_PIPE_CHANCE))[0]
            self.pipe_stack.append( pipe_class(self._screen, self.generate_gap_top(), self._screen.get_width()) )

    # Updates each pipe by moving them.
    # If the last pipe is already having enough distance, generates a new pipe at right edge of screen
    # If there is pipe that is out of left screen boundary, then pop it off
    # Also, checks for the scoring for each pipe.
    def update(self, dt):
        # For each of the pipes, move them by updating
        for pipe in self.pipe_stack:
            pipe.update(dt)

        # Pop the pipes which are out of left screen boundary
        while len(self.pipe_stack) and self.pipe_stack[0].is_out_of_bound():
            self.pipe_stack.pop(0)

        # Generate new pipe if the last one has already enough distance
        if self.pipe_stack[-1].is_enough_distance():
            self.generate_new_pipe()

        # Check scoring
        score_increment = sum(pipe.is_scoring() for pipe in self.pipe_stack)
        self.score += score_increment
        Audio.play_count_start_sfx() if score_increment != 0 else None

    def render(self):
        for pipe in self.pipe_stack:
            pipe.render()

    # Check collision of bird with pipes
    def is_collide(self, other_rect: pygame.Rect):
        return any(pipe.is_collide(other_rect) for pipe in self.pipe_stack)

    # Check for any scoring
    def get_scoring(self):
        return self.score
