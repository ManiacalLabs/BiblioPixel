from bibliopixel import animation, colors


class Strip1(animation.BaseAnimation):
    def step(self, amt=1):
        for i in range(self.layout.numLEDs):
            self.layout.set(i, colors.hue2rgb((i * 4) % 256))


class Strip2(animation.BaseAnimation):
    def step(self, amt=1):
        for i in range(self.layout.numLEDs):
            self.layout.set(i, colors.Black if i % 2 else colors.White)
