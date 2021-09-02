import pygame
import src.CONFIG as CONFIG
import src.CONSTANT as C

class BackgroundRenderer:
    _BACKGROUND_IMG = pygame.image.load( C.BACKGROUND_PATH )
    _GROUND_IMG = pygame.image.load( C.GROUND_PATH )
    _BACKGROUND_SPEED = 1
    _GROUND_SPEED = 2

    _FPS_FONT = pygame.font.SysFont('Arial', 15 )

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock ):
        # Convert images
        BackgroundRenderer._BACKGROUND_IMG = BackgroundRenderer._BACKGROUND_IMG.convert()
        BackgroundRenderer._GROUND_IMG = BackgroundRenderer._GROUND_IMG.convert()

        self._screen = screen
        self._clock = clock
        self.background_rect = BackgroundRenderer._BACKGROUND_IMG.get_rect()
        self.ground_rect = BackgroundRenderer._GROUND_IMG.get_rect()
        self.ground_rect.bottom = self._screen.get_height()

    def update(self, dt):
        self.background_rect.left -= BackgroundRenderer._BACKGROUND_SPEED * round(dt)
        if self.background_rect.left < -self._screen.get_width():
            self.background_rect.left = 0

        self.ground_rect.left -= BackgroundRenderer._GROUND_SPEED * round(dt)
        if self.ground_rect.left < -self._screen.get_width():
            self.ground_rect.left = 0

    # All in one rendering. You may choose to render individually in other cases like in game
    def render(self):
        self.render_background()
        self.render_ground()
        self.render_fps()


    def render_background(self):
        self._screen.blit( BackgroundRenderer._BACKGROUND_IMG, self.background_rect )


    def render_ground(self):
        self._screen.blit(BackgroundRenderer._GROUND_IMG, self.ground_rect)


    def render_fps(self):
        if CONFIG.SHOW_FPS:
            fps = BackgroundRenderer._FPS_FONT.render( f'FPS: {self._clock.get_fps():.0f}', True, C.BLACK )
            self._screen.blit( fps, (5,5) )