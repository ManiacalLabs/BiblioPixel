from bibliopixel import animation, colors

PROJECT = {
    "driver": "simpixel",
    "layout": "strip"
}


class Strip1(animation.BaseAnimation):
    def step(self, amt=1):
        for i in range(self.layout.numLEDs):
            self.layout.set(i, colors.hue2rgb((i * 4) % 256))
