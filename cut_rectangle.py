from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range

class RectangleGCodeGenerator:
    def __init__(self, composer, width, height, origin):
        step = 0.4
        depth = 2
        self.z_seq = feed_range(-step, -depth, step)
        self.mill_rad = 0.6
        self.is_cutout = True
        self.origin = origin
        self.comp = composer
        self.width = width
        self.height = height

    def render_program(self):
        comp = self.comp
        offset = self.mill_rad if self.is_cutout else -self.mill_rad
        y_max = self.height - offset
        x_max = self.width - offset
        comp.set_tfm(self.origin)
        comp.move([offset, offset])
        for z in self.z_seq:
            comp.set_z(z)
            comp.feed([offset, y_max])
            comp.feed([x_max, y_max])
            comp.feed([x_max, offset])
            comp.feed([offset, offset])

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 450.0
    cc.drill_rate = 200.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    p = RectangleGCodeGenerator(comp, 63, 46, Transform2D().translate([15, 7]))
    p.render_program()
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('rect.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
