import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C
import src.utils as utils

import src.Game_CountDownState as Game_CountDownState
import src.GameOverState as GameOverState

from src.Bird import Bird
from src.PipeSystem import PipeSystem


class Game:
    SCORE_FONT = pygame.font.Font( C.FONT_PATH, 25 )

    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, background_renderer):
        self._screen = screen
        self._clock = clock
        self._background_renderer = background_renderer
        self._next_state = self

        self.bird = Bird(self._screen)
        # Note the score is stored inside pipe system too.
        self.pipe_system = PipeSystem(self._screen)

        # Inside Game State consists of several substates, like Countdown, InGame, Paused, Dying...
        self.state = Game_CountDownState.Game_CountDown( self._screen, self._clock, self.bird, self.pipe_system )

    def update_internal_state(self):
        self.state = self.state.get_next_state()
        if self.state is None:
            self._next_state = GameOverState.GameOver(self._screen, self._clock, self._background_renderer,
                                                      self.pipe_system.get_scoring() )

    def handle_input(self):
        self.state.handle_input()

    def update(self, dt):
        self._background_renderer.update( dt )

        # State's job
        self.state.update( dt )


    def render(self):
        # Render background first
        self._background_renderer.render_background()
        # Let internal state render its thing
        self.state.render()
        # Render ground and FPS
        self._background_renderer.render_ground()
        self._background_renderer.render_fps()
        # Render score
        score_txt = Game.SCORE_FONT.render(f'Score: {self.pipe_system.get_scoring()}', True, C.GREEN_1 )
        score_txt = utils.compile_outlines(score_txt, [ (C.BLACK, 4) ])
        self._screen.blit( score_txt, score_txt.get_rect(top=5, right=self._screen.get_width() - 5 ) )

        pygame.display.flip()


    def get_next_state(self):
        return self._next_state


    def run(self):
        dt = self._clock.tick( CONFIG.DESIRED_FPS ) * 0.001 / CONFIG.DESIRED_FRAME_INTERVAL

        # Input
        self.handle_input()

        # Update
        self.update( dt )

        # Render
        self.render()

        # Update Internal state
        self.update_internal_state()
        # Return the next state
        return self.get_next_state()
