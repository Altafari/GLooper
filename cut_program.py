from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from pcontext import PContext, cut_slot, cut_rectangle

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
    pcc = PContext(comp, z_seq[0:2], mill_rad=0.6, is_cutout=True)
    origin = Transform2D()
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
    comp.pause(10000)
    cut_slot(pc, width, h_wm, origin.translate([0, -offset - height - h_margin]))
    cut_rectangle(pcc, width, h_wc, origin.translate([0, -offset - height - cutout]))
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('rects.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
