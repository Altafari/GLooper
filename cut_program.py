from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from pcontext import PContext, cut_slot, cut_rectangle

def cut_slots_at(origin, comp, pc):
    pcc = PContext(comp, z_seq[0:2], mill_rad=pc.mill_rad, is_cutout=True)
    width = 5.1
    height = 8.0
    h_margin = 0.1
    h_wm = height + 2 * h_margin
    offset = 10.0
    cutout = 0.9
    h_wc = height + 2 * cutout
    cut_slot(pc, width, h_wm, origin.translate([0, offset - h_margin]))
    cut_rectangle(pcc, width, h_wc, origin.translate([0, offset - cutout]))
    comp.lift()
    comp.pause(5000)
    cut_slot(pc, width, h_wm, origin.translate([0, -offset - height - h_margin]))
    cut_rectangle(pcc, width, h_wc, origin.translate([0, -offset - height - cutout]))
    comp.lift()
    comp.pause(5000)    

def cut_all_slots(origin, comp, pc):
    offset = 25.0
    origin = origin.translate([20.0 - 0.05, 0])
    for _ in range(10):
        cut_slots_at(origin, comp, pc)
        origin = origin.translate([offset, 0])

def cut_contour(origin, comp, pc):
    mr = pc.mill_rad  
    origin = origin.translate([-mr, 0])  
    length = 25.0 * 9.0 + 40.0 + 2.0 * mr + 5.0
    half_width = 22.0 + mr
    cutout_depth = 2.0
    cutout_width = 5.0 - 2.0 * mr
    cutout_offset = 5.0 + mr
    contour_pts = [[0.0, -half_width],
                   [cutout_offset, -half_width],
                   [cutout_offset, cutout_depth-half_width],
                   [cutout_offset+cutout_width, cutout_depth-half_width],
                   [cutout_offset+cutout_width, -half_width],
                   [length-cutout_offset-cutout_width, -half_width],
                   [length-cutout_offset-cutout_width, cutout_depth-half_width],
                   [length-cutout_offset, cutout_depth-half_width],
                   [length-cutout_offset, -half_width],
                   [length, -half_width],
                   [length, half_width],
                   [length-cutout_offset, half_width],
                   [length-cutout_offset, half_width-cutout_depth],
                   [length-cutout_offset-cutout_width, half_width-cutout_depth],
                   [length-cutout_offset-cutout_width, half_width],
                   [cutout_offset+cutout_width, half_width],
                   [cutout_offset+cutout_width, half_width-cutout_depth],
                   [cutout_offset, half_width-cutout_depth],
                   [cutout_offset, half_width],
                   [0.0, half_width]]
    comp.set_tfm(origin)
    comp.move(contour_pts[-1])
    for z in pc.z_seq:
        comp.set_z(z)
        for pt in contour_pts:
            comp.feed(pt)

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 100.0
    cc.drill_rate = 100.0
    comp = Composer(cc)
    comp.set_spindle(80)
    step = 0.4
    depth = 5.2
    z_seq = feed_range(-step, -depth, step)
    pc = PContext(comp, z_seq, mill_rad=0.6, is_cutout=True)
    origin = Transform2D().translate([0, -23])
    cut_all_slots(origin, comp, pc)
    cut_contour(origin, comp, pc)
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('rects.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
