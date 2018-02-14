"""
DEPRECATED!

This is probably not used and should likely be replaced by the code
in BiblioPixelAnimations.matrix.ImageAnim

"""
def convert_mode(image, mode='RGB'):
    """Return an image in the given mode."""
    return image if (image.mode == mode) else image.convert(mode=mode)


def image_to_colorlist(image, container=list):
    """Given a PIL.Image, returns a ColorList of its pixels."""
    return container(convert_mode(image).getdata())


def animated_gif_to_colorlists(image, container=list):
    """Given an animated GIF, return a list with a colorlist for each frame."""
    from PIL import ImageSequence

    it = ImageSequence.Iterator(image)
    return [image_to_colorlist(i, container) for i in it]
