import pygame
import os.path as path

import src.CONFIG as CONFIG
pygame.init()
screen = pygame.display.set_mode( CONFIG.SCREEN_SIZE )

import src.Audio as Audio

import src.MainMenuState as MainMenuState

from src.BackgroundRenderer import BackgroundRenderer

# An Game instance is a state machine. It has a self.state and will run() it.
class Game:
    def __init__(self):
        self.screen = screen
        pygame.display.set_caption('Flappy Birb')
        pygame.display.set_icon( pygame.image.load( path.join('assets', 'bird.png') ) )
        self.clock = pygame.time.Clock()
        self.bg = BackgroundRenderer(self.screen, self.clock)

        self.state = MainMenuState.MainMenu( self.screen, self.clock, self.bg )

    def start(self):
        # Play BGM
        Audio.play_music()

        while self.state is not None:
            self.state = self.state.run()

        pygame.quit()
        quit()
