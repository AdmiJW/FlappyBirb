import sys
import pygame


# Having a Quit State that is transitioned to whenever the user tries to quit, is a better choice than implementing
# the quitting function them inside each of the states
# This gives us space to add additional features, like autosaving before quit, or some other creative features
# before the game really quits
class Quit:
    def __init__(self):
        pass

    def quit_game(self):
        pygame.quit()
        sys.exit()

    # Both update() and run() does the same thing, to be suited to the different interfaces used.
    def update(self, dt):
        self.quit_game()

    def handle_input(self):
        self.quit_game()

    def run(self):
        self.quit_game()