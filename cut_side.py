from composer import Composer, ComposerConfig
from feedrange import feed_range

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 300.0
    cc.drill_rate = 200.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    step = 0.4
    depth = 1.8
    z_seq = feed_range(-step, -depth, step)
    idx = 0
    coords = [[0, 0], [100, 0]]
    comp.move(coords[0])
    for z in z_seq:
        idx = (idx + 1) % 2
        comp.set_z(z)
        comp.feed(coords[idx])
    comp.cfg.lift_z = 30
    comp.lift()
    comp.set_spindle(0)
    with open('cut_side.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
