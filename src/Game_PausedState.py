import pygame

import src.CONSTANT as C
import src.utils as utils

import src.Audio as Audio

from src.Bird import Bird
from src.PipeSystem import PipeSystem

import src.QuitState as QuitState
import src.Game_CountDownState as Game_CountDownState


class Game_Paused:
    PAUSE_FONT = pygame.font.Font( C.FONT_PATH, 80 )

    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, bird: Bird, pipe_system: PipeSystem ):
        self._screen = screen
        self._clock = clock
        self._bird = bird
        self._pipe_system = pipe_system
        self._next_state = self

        paused_txt = Game_Paused.PAUSE_FONT.render('PAUSED', True, C.GREEN_1 )
        self.paused_txt = utils.compile_outlines( paused_txt, [ (C.GREEN_2, 4), (C.BLACK, 8), (C.WHITE, 4) ] )
        self.paused_txt_rect = self.paused_txt.get_rect( center=self._screen.get_rect().center )


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = QuitState.Quit()
            elif event.type == pygame.KEYDOWN:
                # UnPause
                if event.key == pygame.K_RETURN:
                    self._next_state = Game_CountDownState.Game_CountDown( self._screen, self._clock,
                                                                     self._bird, self._pipe_system )
                    Audio.play_selected_sfx()

    # No updating when paused
    def update(self, dt):
        pass


    def render(self):
        self._bird.render()
        self._pipe_system.render()

        self._screen.blit( self.paused_txt, self.paused_txt_rect )


    def get_next_state(self):
        return self._next_state
