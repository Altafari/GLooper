from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from math import sqrt

class PlateGCodeGenerator:
    def __init__(self, offset, composer, z_offset):
        step = 0.3
        depth = 5.6
        self.z_seq = feed_range(z_offset - step, -depth + z_offset, step)
        self.mill_rad = 0.7
        origin = offset.translate([40.0, 40.0])
        self.origin = origin
        self.comp = composer
        self.four_angles = [origin.rotate(a) for a in range(0, 360, 90)]
        self.six_angles = [origin.rotate(a) for a in range(0, 360, 60)]

    def cut_round_holes(self, radius=11.5, offset=[14.0, 14.0]):
        corr_rad = radius - self.mill_rad
        entry = [offset[0] - corr_rad, offset[1]]
        for t in self.four_angles:
            self.comp.set_tfm(t)
            self.comp.move(entry)
            for z in self.z_seq:
                self.comp.set_z(z)
                self.comp.feed_arc(entry, [corr_rad, 0.0], True)
                self.comp.lift()
                self.comp.pause(1000)
            self.lift_for_cleaning()

    def cut_outer_contour(self, radius=43, offset=37):
        radius_corr = radius + self.mill_rad
        offset_corr = offset + self.mill_rad
        intercept = sqrt(radius_corr * radius_corr - offset_corr * offset_corr)
        entry = [offset_corr, -intercept]
        line_goal = [offset_corr, intercept]
        arc_goal = [intercept, offset_corr]
        self.comp.set_tfm(self.four_angles[0])
        self.comp.move(entry)
        for z in self.z_seq:
            self.comp.set_z(z)
            for t, i in zip(self.four_angles, range(0, 4)):
                self.comp.set_tfm(t)
                if(i % 2 == 0):
                    self.cut_side(offset, intercept)
                else:
                    self.comp.feed(line_goal)
                ctr_off = [-line_goal[0], -line_goal[1]]
                self.comp.feed_arc(arc_goal, ctr_off, False)
            self.comp.lift()
            self.comp.pause(1000)
        self.lift_for_cleaning()

    def cut_side(self, offset, intercept, d1=10.0, h1=8.0, w1=8.0, w2=1.5, t1=1.5, d2=2.0):
        r = self.mill_rad
        x1 = offset + r
        y1 = d1 - r
        x2 = offset + r + h1 - (t1 + w2)
        y2 = y1 + d2
        x3 = x2 + w2 - 2.0*r
        slot = [[x1, y1], [x2, y1], [x2, y2], [x3, y2], [x3, y1]]
        pts = [[x1+h1, y1], [x1+h1, d1+w1+r], [x1, d1+w1+r], [x1, intercept]]
        half_cut = slot + pts
        mirrored_cut = [[x, -y] for x, y in half_cut[::-1]]
        full_cut = mirrored_cut[1:] + half_cut
        for p in full_cut:
            self.comp.feed(p)

    def render_program(self):
        self.cut_round_holes()
        self.cut_outer_contour()
        self.comp.set_tfm(p.origin)

    def lift_for_cleaning(self):
        prev_lift_z = self.comp.cfg.lift_z
        self.comp.cfg.lift_z = 30
        self.comp.set_spindle(0)
        self.comp.lift()
        self.comp.pause(1000)
        self.comp.cfg.lift_z = prev_lift_z
        self.comp.lift()
        self.comp.set_spindle(1000)

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 150.0
    cc.drill_rate = 60.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    for y in range(0, 1):
        for x in range(0, 3):
            offset = [94 * x, 78 * y]
            p = PlateGCodeGenerator(Transform2D().translate(offset), comp, 0)
            p.render_program()
    comp.lift()
    comp.set_spindle(0)
    with open('base_v1.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
