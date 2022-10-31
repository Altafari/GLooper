from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from pcontext import PContext, cut_circle

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 200.0
    cc.drill_rate = 150.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    step = 0.8
    depth = 5.2
    z_seq = feed_range(-step, -depth, step)
    pc = PContext(comp, z_seq, mill_rad=0.5, is_cutout=True)
    radius = 176.0 / 2
    origin = Transform2D().translate([radius + 2.0, radius + 2.0])
    slot_len = 10.0
    slot_offset = 6.5
    for i in range(5):
            p_origin = origin.rotate(72 * i).translate([0, 60])
            cut_circle(pc, 6, p_origin)
    cut_circle(pc, 54, origin)
    pc.is_cutout = False
    cut_circle(pc, radius * 2.0, origin)
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_tfm(Transform2D())
    comp.move([250, 180])
    comp.set_spindle(0)
    with open('base_disk.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
