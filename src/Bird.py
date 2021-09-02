import math

import pygame

import src.CONFIG as CONFIG
import src.CONSTANT as C


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._screen = screen
        self.base_image = pygame.image.load( C.BIRD_PATH ).convert_alpha()
        self.image = self.base_image
        self.centerx = CONFIG.BIRD_LEFT_OFFSET
        self.centery = self._screen.get_height() // 2
        self.rect = self.image.get_rect( center=( self.centerx, self.centery ) )

        self.dy = 0

    @staticmethod
    def get_rotation_angle(dy):
        TV = CONFIG.BIRD_TERMINAL_VELOCITY
        x = math.pi * (dy + TV) / (TV * 2)
        return math.cos( x ) * 45

    # Makes the bird jump by adjusting vertical velocity
    def jump(self):
        self.dy = -CONFIG.BIRD_JUMP_STRENGTH

    # Updates the location of the bird
    # Also applies the rotation to the bird image
    def update(self, dt):
        rotation_angle = Bird.get_rotation_angle(self.dy)

        self.centery += self.dy * dt
        self.dy = min( CONFIG.BIRD_TERMINAL_VELOCITY, self.dy + CONFIG.BIRD_GRAVITY )

        self.image = pygame.transform.rotozoom( self.base_image, rotation_angle, 1 )
        self.rect = self.image.get_rect( center=(self.centerx, self.centery))
        # Shrinks the bounding box because rotated rect is much larger than image
        self.rect.inflate_ip( -12, -18 )


    def render(self):
        # The shrinked rectangle will appear offset, therefore we adjust the offset here
        self._screen.blit( self.image, self.rect.move(-6,-9) )
