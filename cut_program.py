from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range

class GCodeGenerator:
    def __init__(self, composer):
        step = 0.4
        depth = 3.2
        self.z_seq = feed_range(-step, -depth, step)
        self.mill_rad = 0.6
        self.is_cutout = True
        self.comp = composer

    def cut_rectangle(self, width, height, origin):
        comp = self.comp
        offset = self.mill_rad if self.is_cutout else -self.mill_rad
        y_max = height - offset
        x_max = width - offset
        comp.set_tfm(origin)
        comp.move([offset, offset])
        for z in self.z_seq:
            comp.set_z(z)
            comp.feed([offset, y_max])
            comp.feed([x_max, y_max])
            comp.feed([x_max, offset])
            comp.feed([offset, offset])

    def cut_circle(self, diameter, center):
        comp = self.comp
        offset = self.mill_rad if self.is_cutout else -self.mill_rad
        radius = (0.5 * diameter) - offset)
        comp.set_tfm(center)
        start = [radius, 0]
        comp.move(start)
        for z in self.z_seq:
            comp.set_z(z)
            comp.feed_arc(start, [-radius, 0], True)

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 450.0
    cc.drill_rate = 200.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    p = GCodeGenerator(comp)
    p.cut_circle(12.5, Transform2D().translate([110, 30]))
    p.cut_circle(16, Transform2D().translate([127, 15]))
    p.cut_circle(16, Transform2D().translate([127, 45]))
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('rect.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
