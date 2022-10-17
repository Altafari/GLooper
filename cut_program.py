from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from pcontext import PContext, cut_slot

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 300.0
    cc.drill_rate = 200.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    step = 0.4
    depth = 5.3
    z_seq = feed_range(-step, -depth, step)
    pc = PContext(comp, z_seq, mill_rad=0.6, is_cutout=True)
    origin = Transform2D()
    cut_slot(pc, 5, 8, origin.translate([0, 10]))
    cut_slot(pc, 5, 8, origin.flip_y().translate([0, 10]))
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('rects.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
