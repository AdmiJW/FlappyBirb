import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C
import src.utils as utils

import src.Audio as Audio

from src.Bird import Bird
from src.PipeSystem import PipeSystem

import src.QuitState as QuitState
import src.Game_InGameState as Game_InGameState


class Game_CountDown:
    _NUM_FONT = pygame.font.Font( C.FONT_PATH, 80 )
    _GUIDE_FONT = pygame.font.Font( C.FONT_PATH, 35 )

    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, bird: Bird, pipe_system: PipeSystem ):
        self._screen = screen
        self._clock = clock
        self._bird = bird
        self._next_state = self
        self._pipe_system = pipe_system

        self.frame_left = CONFIG.DESIRED_FPS
        self.countdown = 2      # Countdown will be 2,1,0, equivalent to 3,2,1

        centerx, centery = self._screen.get_rect().center

        # Text for countdown
        num_3_txt = Game_CountDown._NUM_FONT.render('3', True, C.GREEN_1)
        num_2_txt = Game_CountDown._NUM_FONT.render('2', True, C.GREEN_1)
        num_1_txt = Game_CountDown._NUM_FONT.render('1', True, C.GREEN_1)
        self.nums = [
            utils.compile_outlines(num_1_txt, [(C.GREEN_2, 4), (C.BLACK, 8), (C.WHITE, 4)]),
            utils.compile_outlines(num_2_txt, [(C.GREEN_2, 4), (C.BLACK, 8), (C.WHITE, 4)]),
            utils.compile_outlines(num_3_txt, [ (C.GREEN_2, 4), (C.BLACK, 8), (C.WHITE, 4) ])
        ]

        # Guide Text
        guide_1_txt = Game_CountDown._GUIDE_FONT.render('Use SPACE/CLICK to Jump', True, C.WHITE)
        guide_2_txt = Game_CountDown._GUIDE_FONT.render('Use ENTER to Pause', True, C.WHITE)
        self.guide_1 = utils.compile_outlines( guide_1_txt, [ (C.BLACK, 4) ] )
        self.guide_2 = utils.compile_outlines( guide_2_txt, [ (C.BLACK, 4) ] )

        self.num_rect = self.nums[0].get_rect( center=(centerx, centery) )
        self.guide_1_rect = self.guide_1.get_rect( center=(centerx, centery+180) )
        self.guide_2_rect = self.guide_2.get_rect(center=(centerx, centery+220))


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = QuitState.Quit()


    def update(self, dt):
        self.frame_left -= dt
        if self.frame_left < 0:
            self.countdown -= 1
            self.frame_left = CONFIG.DESIRED_FPS + self.frame_left

            if self.countdown < 0:
                self._next_state = Game_InGameState.Game_InGame( self._screen, self._clock, self._bird, self._pipe_system )
                Audio.play_count_start_sfx()
            else:
                Audio.play_counting_sfx()


    def render(self):
        self._bird.render()
        self._pipe_system.render()
        self._screen.blit( self.nums[ max(0,self.countdown) ], self.num_rect )
        self._screen.blit( self.guide_1, self.guide_1_rect)
        self._screen.blit( self.guide_2, self.guide_2_rect)

    def get_next_state(self):
        return self._next_state
