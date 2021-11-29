from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from math import sqrt

class PlateGCodeGenerator:
    def __init__(self, origin, diameter, composer, feed_range):
        self.comp = composer
        self.z_seq = feed_range
        self.mill_rad = diameter / 2.0
        self.origin = origin.translate([33.0, 33.0])
        self.four_angles = [self.origin.rotate(a) for a in range(0, 360, 90)]
        self.six_angles = [self.origin.rotate(a) for a in range(0, 360, 60)]

    def cut_hex_hole(self, size=7.0):
        dist = size / sqrt(3) - self.mill_rad
        corner = [0.0, dist]
        self.comp.set_tfm(self.six_angles[-1])
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

def generate_origins(x_dim, x_count, y_dim, y_count):
    return [Transform2D().translate([x*x_dim, y*y_dim]) for y in range(0, y_count) for x in range(0, x_count)]

def cut_preliminary_holes(origins, comp, fr, diam):
    res = []
    for origin in origins:
        p = PlateGCodeGenerator(origin, diam, comp, fr)
        p.cut_hex_hole()
        p.cut_round_holes()
        res += p.comp.program
    return shutdown_and_park(comp, res)

def cut_accurate_hex_holes(origins, comp, fr, diam):
    res = []
    for origin in origins:
        p = PlateGCodeGenerator(origin, diam, comp, fr)
        p.cut_hex_hole()
        res += p.comp.program
    return shutdown_and_park(comp, res)

def cut_final_contours(origins, comp, fr, diam):
    res = []
    for origin in origins:
        p = PlateGCodeGenerator(origin, diam, comp, fr)
        p.cut_outer_contour()
        res += p.comp.program
    return shutdown_and_park(comp, res)

def shutdown_and_park(comp, res):
    comp.program = []
    comp.set_spindle(0)
    comp.set_tfm(Transform2D())
    comp.move([0.0, 0.0])
    return res + comp.program

if __name__ == '__main__':
    origins = generate_origins(66, 1, 66, 1)
    cc = ComposerConfig()
    cc.feed_rate = 240
    cc.drill_rate = 120
    comp = Composer(cc)
    comp.set_spindle(1000)
    fr = [-1.4]
    first_cut = cut_preliminary_holes(origins, comp, fr, 2.2)
    with open('plate_2.2mm_holes.gcode', 'w+') as f:
        f.write('\n'.join(first_cut))
    cc.feed_rate = 60
    cc.drill_rate = 60
    comp = Composer(cc)
    comp.set_spindle(1000)
    fr = feed_range(0, -1.4, 0.2)
    second_cut = cut_accurate_hex_holes(origins, comp, fr, 0.5)
    with open('plate_0.5mm_holes.gcode', 'w+') as f:
        f.write('\n'.join(second_cut))
    cc.feed_rate = 240
    cc.drill_rate = 120
    comp = Composer(cc)
    comp.set_spindle(1000)
    fr = [-1.4]
    third_cut = cut_final_contours(origins, comp, fr, 2.2)
    with open('plate_2.2mm_contour.gcode', 'w+') as f:
        f.write('\n'.join(third_cut))
    

