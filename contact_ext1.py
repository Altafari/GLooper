from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from pcontext import PContext, cut_hex_hole, cut_rectangle, cut_circle

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 200.0
    cc.drill_rate = 150.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    step = 0.4
    depth = 1.2
    z_seq = feed_range(-step, -depth, step)
    pc = PContext(comp, z_seq, mill_rad=0.5, is_cutout=True)
    radius = 15.0
    origin = Transform2D().translate([radius + 3.0, radius + 3.0])
    slot_len = 10.0
    slot_offset = 6.5
    for i in range(2):
        for j in range(1):
            pc.is_cutout = True
            p_origin = origin.translate([i * (radius * 2 + 3.0), j * (radius * 2 + 3.0)])
            cut_hex_hole(pc, 7.0, p_origin)
            s_origin = p_origin.translate([slot_offset, -slot_len / 2.0])
            cut_rectangle(pc, pc.mill_rad * 2, slot_len, s_origin)
            s_origin = p_origin.rotate(180).translate([slot_offset, -slot_len / 2.0])
            cut_rectangle(pc, pc.mill_rad * 2, slot_len, s_origin)
            pc.is_cutout = False
            cut_circle(pc, 2 * radius, p_origin)
    comp.cfg.lift_z = 25
    comp.lift()
    comp.set_spindle(0)
    with open('contact_ext1.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
