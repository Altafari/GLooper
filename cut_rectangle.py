from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from math import sqrt

class RectangleGCodeGenerator:
    def __init__(self, composer, width, height, origin):
        step = 0.2
        depth = 1.3
        self.z_seq = feed_range(-step, -depth, step)
        self.mill_rad = 0.5
        self.origin = origin
        self.comp = composer
        self.width = width
        self.height = height

    def render_program(self):
        comp = self.comp
        y_max = self.height + self.mill_rad * 2
        x_max = self.width + self.mill_rad * 2
        comp.set_tfm(self.origin)
        comp.move([0, 0])
        for z in self.z_seq:
            comp.set_z(z)
            comp.feed([0, y_max])
            comp.feed([x_max, y_max])
            comp.feed([x_max, 0])
            comp.feed([0, 0])

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 450.0
    cc.drill_rate = 200.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    for x in range(0, 3):
        p = RectangleGCodeGenerator(comp, 40, 40, Transform2D().translate([x * 41, 0]))
        p.render_program()
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('rect.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
