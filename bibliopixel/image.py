import sys
import os
os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import log

try:
    from PIL import Image, ImageSequence
except ImportError as e:
    error = "Please install Python Imaging Library: pip install pillow"
    log.logger.error(error)
    raise ImportError(error)

import glob
from led import LEDMatrix
from animation import BaseMatrixAnim
import colors


class ImageAnim(BaseMatrixAnim):

    def _getBufferFromImage(self, img, offset = (0,0)):
        duration = None
        if 'duration' in img.info:
            duration = img.info['duration']

        w = self._led.width - offset[0]
        if img.size[0] < w:
            w = img.size[0]

        h = self._led.height - offset[1]
        if img.size[1] < h:
            h = img.size[1]

        ox = offset[0]
        oy = offset[1]

        buffer = [0 for x in range(self._led.bufByteCount)]
        gamma = self._led.driver[0].gamma
        if self._bgcolor != (0,0,0):
            for i in range(self._led.numLEDs):
                buffer[i*3 + 0] = gamma[self._bgcolor[0]]
                buffer[i*3 + 1] = gamma[self._bgcolor[1]]
                buffer[i*3 + 2] = gamma[self._bgcolor[2]]

        frame = Image.new("RGBA", img.size)
        frame.paste(img)

        for x in range(ox, w + ox):
            for y in range(oy, h + oy):
                pixel = self._led.matrix_map[y][x]
                r, g, b, a = frame.getpixel((x - ox,y - oy))
                if a == 0:
                    r, g, b = self._bgcolor
                else:
                    r = (r * a) >> 8
                    g = (g * a) >> 8
                    b = (b * a) >> 8
                if self._bright != 255:
                    r, g, b = colors.color_scale((r, g, b), self._bright)

                buffer[pixel*3 + 0] = gamma[r]
                buffer[pixel*3 + 1] = gamma[g]
                buffer[pixel*3 + 2] = gamma[b]

        return (duration, buffer)

    def _getBufferFromPath(self, imagePath, offset = (0,0)):
        img = Image.open(imagePath)
        return self._getBufferFromImage(img, offset)

    def __init__(self, led, imagePath, offset = (0,0), bgcolor = colors.Off, brightness = 255):
        """Helper class for displaying image animations for GIF files or a set of bitmaps

        led - LEDMatrix instance
        imagePath - Path to either a single animated GIF image or folder of sequential bitmap files
        offset - X,Y tuple coordinates at which to place the top-left corner of the image
        bgcolor - RGB tuple color to replace any transparent pixels with. Avoids transparent showing as black
        brightness - Brightness value (0-255) to scale the image by. Otherwise uses master brightness at the time of creation
        """
        super(ImageAnim, self).__init__(led)

        self._bright = brightness
        if self._bright == 255 and led.masterBrightness != 255:
            self._bright = led.masterBrightness

        self._bgcolor = colors.color_scale(bgcolor, self._bright)
        self._offset = offset
        self._images = []
        self._count = 0

        if imagePath.endswith(".gif"):
            log.logger.info("Loading {0} ...".format(imagePath))
            img = Image.open(imagePath)
            if self._offset == (0,0):
                w = 0
                h = 0
                if img.size[0] < self._led.width:
                    w = (self._led.width - img.size[0]) / 2
                if img.size[1] < self._led.height:
                    h = (self._led.height - img.size[1]) / 2
                self._offset = (w, h)

            for frame in ImageSequence.Iterator(img):
                self._images.append(self._getBufferFromImage(frame, self._offset))
                self._count += 1
        else:
            imageList = glob.glob(imagePath + "/*.bmp")
            imageList.sort()

            self._count = len(imageList)
            if self._count == 0:
                raise ValueError("No images found!")

            for img in imageList:
                if self._offset == (0,0):
                    if img.size[0] < self._led.width:
                        self._offset[0] = (self._led.width - img.size[0]) / 2
                    if img.size[1] < self._led.height:
                        self._offset[1] = (self._led.height - img.size[1]) / 2

                self._images.append(self._getBufferFromPath(img, self._offset))

        self._curImage = 0
       
    def preRun(self):
        self._curImage = 0

    def step(self, amt = 1):
        self._led.all_off()
        
        self._led.setBuffer(self._images[self._curImage][1])
        self._internalDelay = self._images[self._curImage][0]

        self._curImage += 1
        if self._curImage >= self._count:
            self._curImage = 0
            self.animComplete = True

        self._step = 0


def showImage(led, imagePath = "", imageObj = None, offset = (0,0), bgcolor = colors.Off, brightness = 255):
    """Display an image on the matrix"""

    if not isinstance(led, LEDMatrix):
        raise RuntimeError("Must use LEDMatrix with showImage!")


    bgcolor = colors.color_scale(bgcolor, brightness)

    img = imageObj
    if not img and not (imagePath == ""):
        img = Image.open(imagePath)
    elif not img:
        raise ValueError("Must provide either imagePath or imageObj")

    w = led.width - offset[0]
    if img.size[0] < w:
        w = img.size[0]

    h = led.height - offset[1]
    if img.size[1] < h:
        h = img.size[1]

    ox = offset[0]
    oy = offset[1]

    led.all_off()

    for x in range(ox, w + ox):
        for y in range(oy, h + oy):
            r,g,b,a = (0,0,0,255)
            rgba = img.getpixel((x - ox,y - oy))
            if len(rgba) == 3: r,g,b = rgba
            elif len(rgba) == 4: r,g,b,a = rgba
            else: raise ValueError("Image must be in RGB or RGBA format!");

            if a == 0:
                r, g, b = bgcolor
            else:
                r, g, b = colors.color_scale((r, g, b), a)

            if brightness != 255:
                    r, g, b = colors.color_scale((r, g, b), brightness)

            led.set(x, y, (r, g, b))