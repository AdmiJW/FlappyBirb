import pygame
import src.CONSTANT as C

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(10)


# Loads the BGM of the game
pygame.mixer.music.load( C.MUSIC_PATH )
pygame.mixer.music.set_volume(0.15)

# Load the other sound effects
_CHANGE_SELECTION_SFX = pygame.mixer.Sound( C.CHANGE_SELECTION_PATH )
_COLLISION_SFX = pygame.mixer.Sound( C.COLLISION_PATH )
_COUNT_START_SFX = pygame.mixer.Sound( C.COUNT_START_PATH )
_COUNTING_SFX = pygame.mixer.Sound( C.COUNTING_PATH )
_GAME_OVER_SFX = pygame.mixer.Sound( C.GAME_END_PATH )
_JUMP_SFX = pygame.mixer.Sound( C.JUMP_PATH )
_SELECTED_SFX = pygame.mixer.Sound( C.SELECTED_PATH )

# Changes Volume
_CHANGE_SELECTION_SFX.set_volume(0.25)
_COLLISION_SFX.set_volume(0.25)
_COUNT_START_SFX.set_volume(0.25)
_COUNTING_SFX.set_volume(0.25)
_GAME_OVER_SFX.set_volume(0.25)
_JUMP_SFX.set_volume(0.15)
_SELECTED_SFX.set_volume(0.25)

def play_change_selection_sfx():
    _CHANGE_SELECTION_SFX.play()

def play_collision_sfx():
    _COLLISION_SFX.play()

def play_count_start_sfx():
    _COUNT_START_SFX.play()

def play_counting_sfx():
    _COUNTING_SFX.play()

def play_game_over_sfx():
    _GAME_OVER_SFX.play()

def play_jump_sfx():
    _JUMP_SFX.play()

def play_selected_sfx():
    _SELECTED_SFX.play()

def play_music():
    pygame.mixer.music.play(-1)
