from bibliopixel import animation
from bibliopixel.colors import COLORS

"""
This is an example Animation class which has a single field -
`color` with the default value `COLORS.green`.

You can edit this as you like, add and remove fields and
write Python code in general.
"""


class Example26(animation.BaseAnimation):
    def __init__(
            self, *args,
            # The fields for your class go here!
            color=COLORS.green,

            # End of the fields for your class
            **kwds):
        super().__init__(*args, **kwds)
        self.color = color
        # Your initialization code goes here.

    def step(self, amt=1):
        this_pixel = self.cur_step % len(self.color_list)

        # Set the previous pixel to black.
        self.color_list[this_pixel - 1] = COLORS.black

        # Set this pixel to the color
        self.color_list[this_pixel] = self.color

    #
    # Everything below here is optional, and you can delete it if you aren't
    # using it.
    #

    # pre_run is called right before the animation starts running.
    def pre_run(self):
        super().pre_run()
        # Your code goes here.

    def cleanup(self, clean_layout=True):
        super().cleanup(clean_layout)
        # Your code goes here.


class Example28(Example26):
    def step(self, amt=1):
        this_pixel = self.cur_step % len(self.color_list)

        # Set the previous pixel to black.
        self.color_list[this_pixel - 1] = COLORS.black

        # Set this pixel to the color
        self.color_list[this_pixel] = self.color
        self.color_list[this_pixel - 2] = COLORS.yellow
        self.color_list[this_pixel - 3] = COLORS.black
