from composer import Composer, ComposerConfig
from cut_program import cut_contour
from transform2d import Transform2D
from feedrange import feed_range
from pcontext import PContext, cut_rounded_rectangle

def drill_hole(comp, coord):
    comp.move(coord)
    comp.feed(coord)

def drill_holes(origin, pc):
    pc.comp.set_tfm(origin)
    pc.comp.set_z(pc.z_seq[-1])
    drill_hole(comp, [-2.5, -1.25])
    drill_hole(comp, [0, -1.25])
    drill_hole(comp, [2.5, -1.25])
    drill_hole(comp, [-1.5, 1.25])
    drill_hole(comp, [1.5, 1.25])

def cut_part(origin, pc, width, height):
    drill_holes(origin, pc)
    radius = 0.8
    rect_origin = origin.translate([-width / 2, -height / 2])
    cut_rounded_rectangle(pc, width, height, radius, rect_origin)

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 200.0
    cc.drill_rate = 150.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    step = 0.4
    depth = 1.2
    z_seq = feed_range(-step, -depth, step)
    pc = PContext(comp, z_seq, mill_rad=0.5, is_cutout=False)
    width = 8.0
    height = 5.0
    origin = Transform2D().translate([width / 2 + pc.mill_rad, height / 2 + pc.mill_rad])
    for i in range(4):
        for j in range(12):
            cut_part(origin.translate([i * 11, j * 8]), pc, width, height)
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('contact_pad.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
