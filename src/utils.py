import pygame
#########################
# Utility functions
#########################

# Given an image, will return a new Surface that is the outline of the given image (with provided color, except (0,0,0))
# (0,0,0) is used as set_colorkey, otherwise the outline will have a black background over it.
# If you want a image with outline, consider using below - compile_outlines() function!
def generate_outline(image: pygame.Surface, color=(1,1,1), outline_width=6):
    if color == (0,0,0):
        raise AttributeError('Cannot use color of (0,0,0) in get_outline() method. Consider other colors that are close'
                             'to black if you insist, like (1,1,1)')

    result = pygame.Surface( ( image.get_width() + outline_width, image.get_height() + outline_width) )

    # The mask surface is an image of black and white. Black - Transparent pixels. White - Opaque pixels
    mask = pygame.mask.from_surface(image)
    mask_surface = mask.to_surface()

    # Replace the white parts with the provided color
    mask = pygame.PixelArray(mask_surface)
    mask.replace( (255,255,255), color)     # Replacing white to the provided color
    mask_surface = mask.surface
    del mask
    mask_surface.set_colorkey( (0,0,0) )

    # Blit the outline around the edges
    result.blit( mask_surface, (0, 0) )
    result.blit( mask_surface, (outline_width, 0) )
    result.blit( mask_surface, (0, outline_width) )
    result.blit( mask_surface, (outline_width, outline_width) )
    result.set_colorkey( (0,0,0) )

    return result


# Given an image you wanted to add outline(s), as indicated in outlines list:
#       [ (color1, width1), (color2, width2)... ]
# will return a final Surface which is the image with outlines blitted unders it.
# (Outline will be blitted from left to right in the list, thus leftmost outline is the bottom layer!)
def compile_outlines(image: pygame.Surface, outlines: list[tuple, int]):
    final_surface = image

    for ol in outlines:
        new_layer = generate_outline(final_surface, *ol)
        center = new_layer.get_rect().center
        new_layer.blit( final_surface, final_surface.get_rect(center=center) )
        new_layer.set_colorkey( (0,0,0) )
        final_surface = new_layer

    return final_surface
