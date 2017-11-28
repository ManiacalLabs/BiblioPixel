class *bibliopixel.Matrix*
==========================

Matrix provides methods to control a matrix of pixels, currently with
the assumption that the matrix is built from a single, continuous run of
1-dimensional LED strips. See [[Coordinate
Mapping\|Display-Setup#coordinate-mapping]] for more details. It
inherits from [[Layout]] and provides all of its public methods and
properties. Matrix actually lives at bibliopixel.layout.Matrix but can
be accessed at bibiliopixel.Matrix for convenience.

\_\_init\_\_
^^^^^^^^^^^^

(driver, width = 0, height = 0, coordMap = None, rotation =
MatrixRotation.ROTATE\_0, vert\_flip = False, serpentine = True,
threadedUpdate = False, brightness=255, pixelSize=(1,1))

-  **driver** - A driver class or list of driver classes that inherit
   from bibliopixel.drivers.driver\_base.[[DriverBase]]. See the
   [[Drivers]] page for more info.
-  **width** - width (x-axis) of the matrix. If width *and* height are
   omitted, it will try to calculate the value from
   [[driver.numLEDs\|DriverBase#numleds]] by assuming it is perfectly
   square.
-  **height** - height (y-axis) of the matrix. If width *and* height are
   omitted, it will try to calculate the value from
   [[driver.numLEDs\|DriverBase#numleds]] by assuming it is perfectly
   square.
-  **coordMap** - To be used if the matrix is not arranged in a standard
   pattern to provide a map from (x,y) coordinates to strip index. See
   [[Coordinate Mapping\|Display-Setup#coordinate-mapping]] for more
   details.
-  **rotation** - Amount to rotate matrix coordinate map by in order for
   coordinate (0,0) to be the Top-Left corner of the display. See
   [[Matrix Orientation\|Display-Setup#matrix-orientation]] for more
   details.
-  **vert\_flip** - True to flip the matrix coordinate map on the
   y-axis. See [[Matrix Orientation\|Display-Setup#matrix-orientation]]
   for more details.
-  **serpentine** - If True, the [[coordinate
   map\|Display-Setup#coordinate-mapping]] with follow a serpentine
   patter. Otherwise, each row index will restart at the left side of
   the matrix.
-  **threadedUpdate** - Display updates will run in background thread if
   True. Defaults to False.
-  **brightness** - Default master brightness value, 0-255
-  **pixelSize** - Sets pixel scaling size. For example, if set to (3,3)
   each call to set() will set a 3x3 LED grid.

set
^^^

(x, y, color)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **color** - RGB tuple, (r,g,b), representing the color to set. If a
   texture has been set with [[setTexture\|#setTexture]], color can be
   left off or set to None to use the pixel color from the texture
   instead.

Set value of pixel at (x,y) coordinate to given color or texture color.

setTexture
^^^^^^^^^^

(tex = None)

-  **tex** - Texture matrix to use with set(). Texture must have same
   dimensions as the matrix and be a 2D list of color tuples. Textures
   can be loaded from an image using [[loadImage\|Image
   Module#loadImage]] from bibliopixel.image

Setting a texture will allow calling set() without the color parameter
to use the color value from the same pixel on the texture instead of a
passed in color value. Any below drawing or set function can take None
instead of a color to use the texture.

get
^^^

(x, y)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel

Returns RGB tuple, (r,g,b), if pixel is in bounds. Otherwise returns
(0,0,0).

setHSV
^^^^^^

(x, y, hsv)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **hsv** - 8-bit HSV tuple (h,s,v)

Convenience method for setting color with an 8-bit [[HSV]] tuple value.

setRGB
^^^^^^

(x, y, r, g, b)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **r** - 8-bit (0-255) Red color component.
-  **g** - 8-bit (0-255) Green color component.
-  **b** - 8-bit (0-255) Blue color component.

Convenience method for setting color with individual components instead
of RGB tuple.

drawCircle
^^^^^^^^^^

(x0, y0, r, color=None)

-  **x0** - x coordinate of circle center point
-  **y0** - y coordinate of circle center point
-  **r** - radius of circle
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   circle.

Draws the outline of a circle.

fillCircle
^^^^^^^^^^

(x0, y0, r, color=None)

-  **x0** - x coordinate of circle center point
-  **y0** - y coordinate of circle center point
-  **r** - radius of circle
-  **color** - RGB tuple, (r,g,b), representing the color to fill the
   circle.

Draws a solid circle of the given color.

drawLine
^^^^^^^^

(x0, y0, x1, y1, color=None)

-  **x0** - x coordinate of first point on the line
-  **y0** - y coordinate of first point on the line
-  **x1** - x coordinate of second point on the line
-  **y1** - y coordinate of second point on the line
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   line.

Draws a line between two points with a given color.

drawRect
^^^^^^^^

(x, y, w, h, color=None)

-  **x** - x coordinate of top-left corner of the rectangle
-  **y** - y coordinate of top-left corner of the rectangle
-  **w** - width of the rectangle
-  **h** - height of the rectangle
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   rectangle outline.

Draws a rectangle with the given color.

fillRect
^^^^^^^^

(x, y, w, h, color=None)

-  **x** - x coordinate of top-left corner of the rectangle
-  **y** - y coordinate of top-left corner of the rectangle
-  **w** - width of the rectangle
-  **h** - height of the rectangle
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   rectangle.

Draws a solid rectangle with the given color.

fillScreen
^^^^^^^^^^

(color=None)

-  **color** - RGB tuple, (r,g,b), representing the color fill the
   screen.

Sets every pixel to the given color.

drawRoundRect
^^^^^^^^^^^^^

(x, y, w, h, r, color=None)

-  **x** - x coordinate of top-left corner of the rectangle
-  **y** - y coordinate of top-left corner of the rectangle
-  **w** - width of the rectangle
-  **h** - height of the rectangle
-  **r** - radius of each corner
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   rectangle outline.

Draws a rectangle outline with rounded corners and using the given
color.

fillRoundRect
^^^^^^^^^^^^^

(x, y, w, h, r, color=None)

-  **x** - x coordinate of top-left corner of the rectangle
-  **y** - y coordinate of top-left corner of the rectangle
-  **w** - width of the rectangle
-  **h** - height of the rectangle
-  **r** - radius of each corner
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   rectangle.

Draws a solid rectangle with rounded corners and using the given color.

drawTriangle
^^^^^^^^^^^^

(x0, y0, x1, y1, x2, y2, color=None)

-  **x0** - x cordinate of point 0 of the triangle
-  **y0** - y cordinate of point 0 of the triangle
-  **x1** - x cordinate of point 1 of the triangle
-  **y1** - y cordinate of point 1 of the triangle
-  **x2** - x cordinate of point 2 of the triangle
-  **y2** - y cordinate of point 2 of the triangle
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   rectangle outline.

Draws the outline of a triangle given 3 points and an RGB color tuple.

fillTriangle
^^^^^^^^^^^^

(x0, y0, x1, y1, x2, y2, color=None)

-  **x0** - x cordinate of point 0 of the triangle
-  **y0** - y cordinate of point 0 of the triangle
-  **x1** - x cordinate of point 1 of the triangle
-  **y1** - y cordinate of point 1 of the triangle
-  **x2** - x cordinate of point 2 of the triangle
-  **y2** - y cordinate of point 2 of the triangle
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   rectangle.

Draws a solid triangle given 3 points and an RGB color tuple.

drawChar
^^^^^^^^

(x, y, c, color, bg, size)

-  **x** - x coordinate of the top-left corner of the character
-  **y** - y coordinate of the top-left corner of the character
-  **c** - character to draw (0-255 ASCII values are all valid)
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   character
-  **bg** - RGB tuple, (r,g,b), representing the color to draw the
   character background
-  **size** - Amount to multiple the size of the character by.
   Characters are all monospaced, 8x5 pixels. Size value will multiply
   this size.

Draws a single character at the given point using the font data in
*bibliopixel.font*.

drawText(text, x = 0, y = 0, color = None, bg = colors.Off, size = 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **text** - ASCII string to draw. Newline (:raw-latex:`\n`) characters
   will move the text to the next line. Carriage return
   (:raw-latex:`\r`) is ignored.
-  **x** - x coordinate of the top-left corner of the character
-  **y** - y coordinate of the top-left corner of the character
-  **color** - RGB tuple, (r,g,b), representing the color to draw the
   text
-  **bg** - RGB tuple, (r,g,b), representing the color to draw the text
   background
-  **size** - Amount to multiple the size of each character by.
   Characters are all monospaced, 8x5 pixels. Size value will multiply
   this size. Size 0 is also now available which is a 6x4 monospaced
   font.

Draws a text string starting at the given point using the font data in
*bibliopixel.font*.

Properties
~~~~~~~~~~

--------------

width
^^^^^

Width of the display matrix

height
^^^^^^

Height of the display matrix

matrix\_map
^^^^^^^^^^^

Generated or provided coordinate map. See [[Coordinate
Mapping\|Display-Setup#coordinate-mapping]] for more details.
