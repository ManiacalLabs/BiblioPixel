Display Setup
=============

Coordinate Mapping
------------------

For [[Strip]] setup, skip to `Channel Order <#channel-order>`__.

When using the [[Matrix]] class, the pixel data is internally stored as
a 1-dimensional list and it needs to know how to map from 2 dimensions
to 1.

By default, it is assumed that a serpentine pattern is used and
coordinate (0,0) is the top left corner of the matrix and that the data
input of the LED strip starts from there, moving to the right across the
top row, and then moving back towards the left on the second row,
continuing to alternate from there. The indices of each pixel on the
strip would then map to the (x,y) coordinates of the matrix, as shown
below.

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <th>

(x,y)

.. raw:: html

   </th>

.. raw:: html

   <th>

0

.. raw:: html

   </th>

.. raw:: html

   <th>

1

.. raw:: html

   </th>

.. raw:: html

   <th>

2

.. raw:: html

   </th>

.. raw:: html

   <th>

3

.. raw:: html

   </th>

.. raw:: html

   <th>

4

.. raw:: html

   </th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

0

.. raw:: html

   </td>

.. raw:: html

   <td>

0

.. raw:: html

   </td>

.. raw:: html

   <td>

1

.. raw:: html

   </td>

.. raw:: html

   <td>

2

.. raw:: html

   </td>

.. raw:: html

   <td>

3

.. raw:: html

   </td>

.. raw:: html

   <td>

4

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

1

.. raw:: html

   </td>

.. raw:: html

   <td>

9

.. raw:: html

   </td>

.. raw:: html

   <td>

8

.. raw:: html

   </td>

.. raw:: html

   <td>

7

.. raw:: html

   </td>

.. raw:: html

   <td>

6

.. raw:: html

   </td>

.. raw:: html

   <td>

5

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

2

.. raw:: html

   </td>

.. raw:: html

   <td>

10

.. raw:: html

   </td>

.. raw:: html

   <td>

11

.. raw:: html

   </td>

.. raw:: html

   <td>

12

.. raw:: html

   </td>

.. raw:: html

   <td>

13

.. raw:: html

   </td>

.. raw:: html

   <td>

14

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

3

.. raw:: html

   </td>

.. raw:: html

   <td>

19

.. raw:: html

   </td>

.. raw:: html

   <td>

18

.. raw:: html

   </td>

.. raw:: html

   <td>

17

.. raw:: html

   </td>

.. raw:: html

   <td>

16

.. raw:: html

   </td>

.. raw:: html

   <td>

15

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

4

.. raw:: html

   </td>

.. raw:: html

   <td>

20

.. raw:: html

   </td>

.. raw:: html

   <td>

21

.. raw:: html

   </td>

.. raw:: html

   <td>

22

.. raw:: html

   </td>

.. raw:: html

   <td>

23

.. raw:: html

   </td>

.. raw:: html

   <td>

24

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

If, however, the minimum row index is always on the left of the matrix;
the [[Matrix]] [[serpentine parameter\|Matrix#\ **init**]] should be set
to False. In this case, the coordinate map will be generated as follows:

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <th>

(x,y)

.. raw:: html

   </th>

.. raw:: html

   <th>

0

.. raw:: html

   </th>

.. raw:: html

   <th>

1

.. raw:: html

   </th>

.. raw:: html

   <th>

2

.. raw:: html

   </th>

.. raw:: html

   <th>

3

.. raw:: html

   </th>

.. raw:: html

   <th>

4

.. raw:: html

   </th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

0

.. raw:: html

   </td>

.. raw:: html

   <td>

0

.. raw:: html

   </td>

.. raw:: html

   <td>

1

.. raw:: html

   </td>

.. raw:: html

   <td>

2

.. raw:: html

   </td>

.. raw:: html

   <td>

3

.. raw:: html

   </td>

.. raw:: html

   <td>

4

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

1

.. raw:: html

   </td>

.. raw:: html

   <td>

5

.. raw:: html

   </td>

.. raw:: html

   <td>

6

.. raw:: html

   </td>

.. raw:: html

   <td>

7

.. raw:: html

   </td>

.. raw:: html

   <td>

8

.. raw:: html

   </td>

.. raw:: html

   <td>

9

.. raw:: html

   </td>

</tr

.. raw:: html

   <tr>

.. raw:: html

   <td>

2

.. raw:: html

   </td>

.. raw:: html

   <td>

10

.. raw:: html

   </td>

.. raw:: html

   <td>

11

.. raw:: html

   </td>

.. raw:: html

   <td>

12

.. raw:: html

   </td>

.. raw:: html

   <td>

13

.. raw:: html

   </td>

.. raw:: html

   <td>

14

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

3

.. raw:: html

   </td>

.. raw:: html

   <td>

15

.. raw:: html

   </td>

.. raw:: html

   <td>

16

.. raw:: html

   </td>

.. raw:: html

   <td>

17

.. raw:: html

   </td>

.. raw:: html

   <td>

18

.. raw:: html

   </td>

.. raw:: html

   <td>

19

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

4

.. raw:: html

   </td>

.. raw:: html

   <td>

20

.. raw:: html

   </td>

.. raw:: html

   <td>

21

.. raw:: html

   </td>

.. raw:: html

   <td>

22

.. raw:: html

   </td>

.. raw:: html

   <td>

23

.. raw:: html

   </td>

.. raw:: html

   <td>

24

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

As long as the matrix follows either of these general layouts, other
than by rotation or being mirrored, the coordinate map will be
automatically generated by [[Matrix]] based on the supplied width,
height, and serpentine parameters.

The coordinate mapping can, however, be overridden by passing a new
coordinate map to the *coordMap* parameter of the [[Matrix]]
[[**init**\ \|Matrix#\ **init**]] method. The coordinate map should be
in the form of a list of lists, like the following:

.. code:: python

    coords = [
        [0,1,2],
        [3,4,5],
        [6,7,8]
    ]

This would define coordinates where the indicies always start back on
the left side as opposed to alternating direction throughout the matrix.

This is particularly useful when combining multiple matrix displays into
one, such as a 16x16 matrix comprised of four `NeoPixel 8x8
Matricies <http://www.adafruit.com/products/1487>`__. These displays use
a non-serpentine pattern as described above, but connecting four of them
in a square will mean that pattern only applies to each quadrant. A
simplified version of this is shown in the table below:

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <th>

0

.. raw:: html

   </th>

.. raw:: html

   <th>

1

.. raw:: html

   </th>

.. raw:: html

   <th>

2

.. raw:: html

   </th>

.. raw:: html

   <th>

9

.. raw:: html

   </th>

.. raw:: html

   <th>

10

.. raw:: html

   </th>

.. raw:: html

   <th>

11

.. raw:: html

   </th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

3

.. raw:: html

   </td>

.. raw:: html

   <td>

4

.. raw:: html

   </td>

.. raw:: html

   <td>

5

.. raw:: html

   </td>

.. raw:: html

   <td>

12

.. raw:: html

   </td>

.. raw:: html

   <td>

13

.. raw:: html

   </td>

.. raw:: html

   <td>

14

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

6

.. raw:: html

   </td>

.. raw:: html

   <td>

7

.. raw:: html

   </td>

.. raw:: html

   <td>

8

.. raw:: html

   </td>

.. raw:: html

   <td>

15

.. raw:: html

   </td>

.. raw:: html

   <td>

16

.. raw:: html

   </td>

.. raw:: html

   <td>

17

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

18

.. raw:: html

   </td>

.. raw:: html

   <td>

19

.. raw:: html

   </td>

.. raw:: html

   <td>

20

.. raw:: html

   </td>

.. raw:: html

   <td>

27

.. raw:: html

   </td>

.. raw:: html

   <td>

28

.. raw:: html

   </td>

.. raw:: html

   <td>

29

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

21

.. raw:: html

   </td>

.. raw:: html

   <td>

22

.. raw:: html

   </td>

.. raw:: html

   <td>

23

.. raw:: html

   </td>

.. raw:: html

   <td>

30

.. raw:: html

   </td>

.. raw:: html

   <td>

31

.. raw:: html

   </td>

.. raw:: html

   <td>

32

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

24

.. raw:: html

   </td>

.. raw:: html

   <td>

25

.. raw:: html

   </td>

.. raw:: html

   <td>

26

.. raw:: html

   </td>

.. raw:: html

   <td>

33

.. raw:: html

   </td>

.. raw:: html

   <td>

34

.. raw:: html

   </td>

.. raw:: html

   <td>

35

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

The indices in the table correspond the actual order of the LEDs in the
display, but this will allow given (X,Y) coordinates to map to the
correct LED. In python it would look like this:

.. code:: python

    coords = [
        [0,1,2,9,10,11],
        [3,4,5,12,13,14],
        [6,7,8,15,16,17],
        [18,19,20,27,28,29],
        [21,22,23,30,31,32]
        [24,25,26,33,34,35]
    ]

    led = Matrix(driver, width = 6, height = 6, coordMap = coords)

If rotation or flip parameters are supplied, those transforms will also
be applied to a supplied coordMap.

MultiMapBuilder and mapGen
--------------------------

To ease this process a bit, we've added the MultiMapBuilder class and
mapGen function. mapGen() will automatically generate a coordinate map
based on the given width, height, and orientation. MultiMapBuilder takes
these coordinate maps and merges them together into a single coordinate
map, automatically increasing the index values.

.. code:: python

    from bibliopixel.layout.multimap import MultiMapBuilder
    from bibliopixel.layout.geometry.matrix import gen_matrix
    build = MultiMapBuilder()
    build.addRow(gen_matrix(4,4), gen_matrix(4,4))
    build.addRow(gen_matrix(8,4))

    led = Matrix(driver, width = 8, height = 8, coordMap = build.map)

The above code represents two 4x4 matrices in the top row and a single
4x8 matrix on the bottom, comprising a single 8x8 matrix. See the
generated matrix map below and note that indices do not represent a
normal 8x8 layout, but instead divided into 3 connected segments (it has
been formatted to accentuate this).

.. code:: python

    [[0, 1, 2, 3,       16, 17, 18, 19],
     [7, 6, 5, 4,       23, 22, 21, 20],
     [8, 9, 10, 11,     24, 25, 26, 27],
     [15, 14, 13, 12,   31, 30, 29, 28],

     [32, 33, 34, 35, 36, 37, 38, 39],
     [47, 46, 45, 44, 43, 42, 41, 40],
     [48, 49, 50, 51, 52, 53, 54, 55],
     [63, 62, 61, 60, 59, 58, 57, 56]]

Matrix Orientation
------------------

For [[Strip]] setup, skip to `Channel Order <#channel-order>`__.

The [[Matrix]] class also accepts rotation and flip parameters which
allow reorienting the display in software so that the (0,0) coordinate
is in the top-left corner.

The following enumeration is provided for setting the rotation of a
matrix:

.. code:: python

    # bibliopixel.layout.Rotation
    class Rotation:
        ROTATE_0 = 0  # no rotation
        ROTATE_90 = 3  # rotate 90 degrees
        ROTATE_180 = 2  # rotate 180 degrees
        ROTATE_270 = 1  # rotate 270 degrees

To complete any needed orientation transforms there is also the
*vert\_flip* parameter which will mirror the display along the x-axis if
set to True. There is no horizontal flip parameter provided as this can
be achieved by setting rotation to 180° and vertical flip to True.

To help through figuring out any needed rotation or flip, the
MatrixOrientationTest animation is provided in the
[[animation\|Animations]] module.

.. code:: python

    from bibliopixel.layout import *
    from bibliopixel.animation import MatrixCalibrationTest
    from bibliopixel.drivers.LPD8806 import *
    from bibliopixel.layout import Rotation

    #create driver for a 12x12 grid, use the size of your display
    driver = LPD8806(12*12)
    led = Matrix(driver)

    anim = MatrixCalibrationTest(led)
    anim.run()

If the display is physically oriented correctly, you should see an
animation starting from the top left and the colored lines should be
vertical, like this:

[[img/0\_noflip.gif]]

But if, for example, you saw this:

[[img/270\_noflip.gif]]

The display needs to be rotated 90° clockwise, so the [[Matrix]]
instance needs to be configured like this:

.. code:: python

    led = Matrix(driver, rotation = Rotation.ROTATE_90)

But if, instead, what you see looks like this:

[[img/180\_flip.gif]]

The display needs to be rotated 180° *and* flipped on the vertical:

.. code:: python

    led = Matrix(driver, rotation = Rotation.ROTATE_180, vert_flip = True)

To aid in the process, match what your display looks like running
MatrixCalibrationTest with the table below. Then use the provided
rotation and flip parameters on your [[Matrix]] init.

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <td>

[[img/0\_noflip.gif]]rotation = Rotation.ROTATE\_0

.. raw:: html

   </td>

.. raw:: html

   <td>

[[img/270\_noflip.gif]]rotation = Rotation.ROTATE\_90

.. raw:: html

   </td>

.. raw:: html

   <tr>

.. raw:: html

   </tr>

.. raw:: html

   <td>

[[img/180\_noflip.gif]]rotation = Rotation.ROTATE\_180

.. raw:: html

   </td>

.. raw:: html

   <td>

[[img/90\_noflip.gif]]rotation = Rotation.ROTATE\_270

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

[[img/0\_flip.gif]]rotation = Rotation.ROTATE\_0, vert\_flip = True

.. raw:: html

   </td>

.. raw:: html

   <td>

[[img/270\_flip.gif]]rotation = Rotation.ROTATE\_90, vert\_flip = True

.. raw:: html

   </td>

.. raw:: html

   <tr>

.. raw:: html

   </tr>

.. raw:: html

   <td>

[[img/180\_flip.gif]]rotation = Rotation.ROTATE\_180, vert\_flip = True

.. raw:: html

   </td>

.. raw:: html

   <td>

[[img/90\_flip.gif]]rotation = Rotation.ROTATE\_270, vert\_flip = True

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Note: To achieve a horizontal flip, rotate 180° *and* flip vertically.

.. code:: python

    rotation = Rotation.ROTATE_180, vert_flip = True

Channel Order
-------------

The last step is to check that the color channel order is correct (if
supported by your chosen driver). Two animations are provided for this
purposed; MatrixCalibrationTest (shown above) and StripChannelTest.

For [[Matrix]] run the following test code.

.. code:: python

    from bibliopixel.led import *
    from bibliopixel.animation import MatrixCalibrationTest
    from bibliopixel.drivers.LPD8806 import *

    #create driver for a 12x12 grid, use the size of your display
    driver = LPD8806(12*12)
    led = Matrix(driver)

    anim = MatrixCalibrationTest(led)
    anim.run()

It should display something like this:

[[img/0\_noflip.gif]]

For [[Strip]] run the following test code.

.. code:: python

    from bibliopixel.led import *
    from bibliopixel.animation import StripChannelTest
    from bibliopixel.drivers.LPD8806 import *

    #create driver for a 12 pixels
    driver = LPD8806(12)
    led = Strip(driver)

    anim = StripChannelTest(led)
    anim.run()

It should display something like this:

[[img/strip\_channel.gif]]

If the RGB ordering is correct, the pattern should start with 1 red led,
2 green leds, and 3 blue leds. If you see different colors, the count of
each color tells you what the position for that color in the channel
order. So, for example, if you see 1 Blue, and 2 Red, and 3 Green leds
then the channel order should be BRG (Blue, Red, Green) and the driver
should be configured as such:

.. code:: python

    driver = LPD8806(num, c_order = ChannelOrder.BRG)

The ChannelOrder enumeration lives in
[[bibliopixel.drivers.driver\_base\|DriverBase]] and contains options
for all six possible channel orders.
