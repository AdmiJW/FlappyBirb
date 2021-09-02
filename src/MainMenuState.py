import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C
import src.utils as utils

import src.Audio as Audio

import src.GameState as GameState
import src.QuitState as QuitState

# Things left to DO:
# - On select start game, return game state
# - Cleaner code?
# - Sound System

class MainMenu:
    _NUM_CHOICES = 3
    _TITLE_FONT = pygame.font.Font(C.FONT_PATH, 70)
    _SUB_FONT = pygame.font.Font(C.FONT_PATH, 40)
    _TUNED_DOWN_FPS = 30

    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, background_renderer):
        self._screen = screen
        self._clock = clock
        self._background_renderer = background_renderer
        self._next_state = self

        # Currently selected choice in Menu
        self._choice = 0

        centerx, centery = self._screen.get_rect().center

        # Title
        title_text = MainMenu._TITLE_FONT.render("FLAPPY BIRB", True, C.GREEN_1)
        self._title = utils.compile_outlines(title_text, [  (C.GREEN_2, 4), (C.BLACK, 8), (C.WHITE, 4) ] )
        self._title_rect = self._title.get_rect( center=( centerx, centery - 150) )

        # Menu Options
        option1_text = MainMenu._SUB_FONT.render('Start Game', True, C.GREEN_1)
        option2_text = MainMenu._SUB_FONT.render('Show/Hide FPS', True, C.GREEN_1)
        option3_text = MainMenu._SUB_FONT.render('Quit', True, C.GREEN_1)
        self._option1 = utils.compile_outlines(option1_text, [ (C.BLACK, 4) ] )
        self._option2 = utils.compile_outlines(option2_text, [(C.BLACK, 4)])
        self._option3 = utils.compile_outlines(option3_text, [(C.BLACK, 4)])

        self._option1_rect = self._option1.get_rect( center=(centerx, centery + 60) )
        self._option2_rect = self._option2.get_rect(center=(centerx, centery + 120))
        self._option3_rect = self._option3.get_rect(center=(centerx, centery + 180))


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = QuitState.Quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self._choice = (self._choice + 1) % MainMenu._NUM_CHOICES
                    Audio.play_change_selection_sfx()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    self._choice = MainMenu._NUM_CHOICES - 1 if self._choice - 1 < 0 else self._choice - 1
                    Audio.play_change_selection_sfx()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Determine next action based on current choice in main menu
                    if self._choice == 0:
                        self._next_state = GameState.Game( self._screen, self._clock, self._background_renderer )
                    elif self._choice == 1:
                        CONFIG.SHOW_FPS = not CONFIG.SHOW_FPS
                    else:
                        self._next_state = QuitState.Quit()
                    Audio.play_selected_sfx()

    def update(self, dt):
        self._background_renderer.update( dt )


    def render(self):
        # Render background first
        self._background_renderer.render()

        # Render title and text
        self._screen.blit( self._title, self._title_rect )
        self._screen.blit(self._option1, self._option1_rect)
        self._screen.blit(self._option2, self._option2_rect)
        self._screen.blit(self._option3, self._option3_rect)

        # Highlighted option
        if self._choice == 0:
            pygame.draw.circle( self._screen, C.BLACK, (self._option1_rect.left - 30, self._option1_rect.centery), 10)
            pygame.draw.circle( self._screen, C.RED, (self._option1_rect.left - 30, self._option1_rect.centery), 8)
        elif self._choice == 1:
            pygame.draw.circle(self._screen, C.BLACK, (self._option2_rect.left - 30, self._option2_rect.centery), 10)
            pygame.draw.circle(self._screen, C.RED, (self._option2_rect.left - 30, self._option2_rect.centery), 8)
        else:
            pygame.draw.circle(self._screen, C.BLACK, (self._option3_rect.left - 30, self._option3_rect.centery), 10)
            pygame.draw.circle(self._screen, C.RED, (self._option3_rect.left - 30, self._option3_rect.centery), 8)

        pygame.display.flip()

    def get_next_state(self):
        return self._next_state

    def run(self):
        fps = MainMenu._TUNED_DOWN_FPS or CONFIG.DESIRED_FPS
        dt = self._clock.tick( fps ) * 0.001 / CONFIG.DESIRED_FRAME_INTERVAL

        # Input
        self.handle_input()

        # Update
        self.update( dt )

        # Render
        self.render()

        # Return next state
        return self.get_next_state()
