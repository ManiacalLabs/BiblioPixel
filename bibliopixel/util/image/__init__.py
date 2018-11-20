from .. import deprecated
if deprecated.allowed():  # pragma: no cover
    from . reshape import crop, resize
    from . load_image import show_image, showImage, loadImage
    from . gif import (
        animated_gif_to_colorlists, convert_mode, image_to_colorlist)
