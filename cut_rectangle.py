from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from math import sqrt

class RectangleGCodeGenerator:
    def __init__(self, composer, width, height):
        step = 0.4
        depth = 2
        self.z_seq = feed_range(-step, -depth, step)
        self.mill_rad = 0.5
        self.origin = Transform2D()
        self.comp = composer
        self.width = width
        self.height = height

    def render_program(self):
        comp = self.comp
        y_max = self.height + self.mill_rad * 2
        x_max = self.width + self.mill_rad * 2
        comp.move([0, 0])
        for z in self.z_seq:
            comp.set_z(z)
            comp.feed([0, y_max])
            comp.feed([x_max, y_max])
            comp.feed([x_max, 0])
            comp.feed([0, 0])
        self.comp.set_tfm(self.origin)

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 450.0
    cc.drill_rate = 60.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    p = RectangleGCodeGenerator(comp, 20, 50)
    p.render_program()
    comp.lift()
    comp.set_spindle(0)
    with open('rect.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
