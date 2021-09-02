import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C

class Pipe(pygame.sprite.Sprite):
    _PIPE_IMAGE_BOTTOM = pygame.image.load( C.PIPE_PATH ).convert_alpha()
    _PIPE_IMAGE_TOP = pygame.transform.flip( _PIPE_IMAGE_BOTTOM, False, True ).convert_alpha()

    def __init__(self, screen: pygame.Surface, gap_top: int, left: int):
        super().__init__()
        self._screen = screen
        self._top_pipe_rect = Pipe._PIPE_IMAGE_TOP.get_rect(left=left, bottom=gap_top)
        self._bottom_pipe_rect = Pipe._PIPE_IMAGE_BOTTOM.get_rect(left=left, top=gap_top+CONFIG.PIPE_GAP)
        self._is_scored = False


    # Returns True once the bird passes the pipe, and only returns it once (never after returned True)
    def is_scoring(self):
        if self._top_pipe_rect.centerx <= CONFIG.BIRD_LEFT_OFFSET and not self._is_scored:
            self._is_scored = True
            return True
        return False


    def is_out_of_bound(self):
        return self._top_pipe_rect.right <= 0


    def is_enough_distance(self):
        return self._top_pipe_rect.right <= self._screen.get_width() - CONFIG.PIPE_DISTANCE


    def update(self, dt):
        self._top_pipe_rect.left -= round(CONFIG.PIPE_SPEED * dt)
        self._bottom_pipe_rect.left -= round(CONFIG.PIPE_SPEED * dt)


    def render(self):
        self._screen.blit( Pipe._PIPE_IMAGE_TOP, self._top_pipe_rect )
        self._screen.blit( Pipe._PIPE_IMAGE_BOTTOM, self._bottom_pipe_rect )


    def is_collide(self, other_rect: pygame.Rect):
        return self._top_pipe_rect.colliderect(other_rect) or self._bottom_pipe_rect.colliderect(other_rect)