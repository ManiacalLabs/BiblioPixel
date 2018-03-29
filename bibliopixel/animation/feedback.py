import copy
from . wrapper import Wrapper
from .. util import color_list


class Feedback(Wrapper):
    def __init__(self, *args, animation,
                 master=1, inputs=None, outputs=None, **kwds):
        super().__init__(*args, animation=animation, **kwds)
        self.master = master

        inputs = inputs or [0]
        outputs = outputs or []

        in_sources = [copy.deepcopy(self.color_list) for i in inputs[1:]]
        in_sources.insert(self.animation.color_list)

        out_sources = [copy.deepcopy(self.color_list) for i in outputs]

        self.inputs = color_list.Mixer(self.color_list, in_sources, inputs)
        self.outputs = color_list.Mixer(self.color_list, out_sources, outputs)

        self.clear = self.inputs.clear
        self.math = self.inputs.math

    def step(self, amt=1):
        super().step(amt=amt)

        self.clear()
        self.inputs.mix(self.master)
        self.outputs.mix(self.master)

        def rotate(sources, begin):
            if len(sources) > 1 + begin:
                sources.insert(begin, sources.pop())

        ins, outs = self.inputs.sources, self.outputs.sources

        rotate(ins, 1)
        rotate(outs, 0)

        if len(ins) > 1:
            self.math.copy(ins[1], ins[0])

        if len(outs) > 0:
            self.math.copy(outs[0], self.color_list)
