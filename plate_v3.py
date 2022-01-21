from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from math import sqrt

class PlateGCodeGenerator:
    def __init__(self, offset, composer):
        self.z_seq = feed_range(0, -1.35, 0.45)
        self.mill_rad = 0.5
        origin = offset.translate([33.0, 33.0])
        self.origin = origin
        self.comp = composer
        self.four_angles = [origin.rotate(a) for a in range(0, 360, 90)]
        self.six_angles = [origin.rotate(a) for a in range(0, 360, 60)]

    def cut_hex_hole(self, size=7.0):
        dist = size / sqrt(3) - self.mill_rad
        corner = [0.0, dist]
        self.comp.set_tfm(self.four_angles[0])
        self.comp.move(corner)
        for z in self.z_seq:
            self.comp.set_z(z)
            for t in self.six_angles:
                self.comp.set_tfm(t)
                self.comp.feed(corner)
    
    def cut_round_holes(self, radius=10.5, offset=[14.0, 14.0]):
        corr_rad = radius - self.mill_rad
        entry = [offset[0] - corr_rad, offset[1]]
        for t in self.four_angles:
            self.comp.set_tfm(t)
            self.comp.move(entry)
            for z in self.z_seq:
                self.comp.set_z(z)
                self.comp.feed_arc(entry, [corr_rad, 0.0], True)
            self.lift_for_cleaning()
                
    def cut_outer_contour(self, radius=36, offset=30):
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
            for t in self.four_angles:
                self.comp.set_tfm(t)
                self.comp.feed(line_goal)
                ctr_off = [-line_goal[0], -line_goal[1]]
                self.comp.feed_arc(arc_goal, ctr_off, False)

    def lift_for_cleaning(self):
        return
        prev_lift_z = self.comp.cfg.lift_z
        self.comp.cfg.lift_z = 35
        self.comp.set_spindle(0)
        self.comp.lift()
        self.comp.cfg.lift_z = prev_lift_z
        self.comp.lift()
        self.comp.set_spindle(1000)

    def render_program(self):
        self.cut_hex_hole()
        self.lift_for_cleaning()
        self.cut_round_holes()
        self.cut_outer_contour()
        self.lift_for_cleaning()
        self.comp.set_tfm(p.origin)
                
if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 180.0
    cc.drill_rate = 120.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    for x in range(0, 4):
        offset = [63 * x, 0]
        p = PlateGCodeGenerator(Transform2D().translate(offset), comp)
        p.render_program()
    comp.lift()
    comp.set_spindle(0)
    with open('plate_v3.gcode', 'w+') as f:
        f.write('\n'.join(comp.program))
