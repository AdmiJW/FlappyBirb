import pygame
import src.utils as utils
import src.CONFIG as CONFIG
import src.CONSTANT as C

import src.Audio as Audio

import src.MainMenuState as MainMenuState
import src.QuitState as QuitState


class GameOver:
    _LG_FONT = pygame.font.Font(C.FONT_PATH, 80)
    _XL_FONT = pygame.font.Font(C.FONT_PATH, 90)
    _MD_FONT = pygame.font.Font(C.FONT_PATH, 35)
    _TUNED_DOWN_FPS = 30

    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, background_renderer, final_score):
        self._screen = screen
        self._clock = clock
        self._background_renderer = background_renderer
        self._next_state = self
        self._final_score = final_score

        centerx, centery = self._screen.get_rect().center

        # Texts
        title_text = GameOver._LG_FONT.render('GAME OVER', True, C.GREEN_1)
        self._title = utils.compile_outlines(title_text, [ (C.GREEN_2, 6), (C.BLACK, 10), (C.WHITE, 4) ])
        score_sign_text = GameOver._MD_FONT.render('Your Final Score: ', True, C.GREEN_1)
        self._score_sign = utils.compile_outlines(score_sign_text, [ (C.BLACK, 6) ])
        score_text = GameOver._XL_FONT.render(str(self._final_score), True, C.GREEN_1)
        self._score = utils.compile_outlines(score_text, [ (C.GREEN_2, 6), (C.BLACK, 10), (C.WHITE, 4) ])
        prompt1_text = GameOver._MD_FONT.render('Press Space/Enter', True, C.GREEN_1)
        self._prompt1 = utils.compile_outlines(prompt1_text, [ (C.BLACK, 4) ] )
        prompt2_text = GameOver._MD_FONT.render('to go back to Main Menu', True, C.GREEN_1)
        self._prompt2 = utils.compile_outlines(prompt2_text, [ (C.BLACK, 4) ] )

        self._title_rect = self._title.get_rect( center=(centerx, centery - 200) )
        self._score_txt_rect = self._score_sign.get_rect( center=(centerx, centery - 100) )
        self._score_rect = self._score.get_rect( center=(centerx, centery) )
        self._prompt_rect = self._prompt1.get_rect( center=(centerx, centery + 220) )
        self._prompt2_rect = self._prompt2.get_rect(center=(centerx, centery + 260) )

        # Play Game Over sound
        Audio.play_game_over_sfx()


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = QuitState.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._next_state = MainMenuState.MainMenu( self._screen, self._clock, self._background_renderer )
                    Audio.play_selected_sfx()

    def update(self, dt):
        self._background_renderer.update(dt)

    def render(self):
        self._background_renderer.render()

        # Render the texts
        self._screen.blit( self._title, self._title_rect)
        self._screen.blit( self._score_sign, self._score_txt_rect )
        self._screen.blit(self._score, self._score_rect)
        self._screen.blit(self._prompt1, self._prompt_rect)
        self._screen.blit(self._prompt2, self._prompt2_rect)

        pygame.display.flip()

    def get_next_state(self):
        return self._next_state

    def run(self):
        fps = GameOver._TUNED_DOWN_FPS or CONFIG.DESIRED_FPS
        dt = self._clock.tick(fps) * 0.001 / CONFIG.DESIRED_FRAME_INTERVAL

        # Input
        self.handle_input()

        # Logic
        self.update(dt)

        # Render
        self.render()

        # Return next state
        return self.get_next_state()


