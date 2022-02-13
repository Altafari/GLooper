from composer import Composer, ComposerConfig
from feedrange import feed_range

if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 150.0
    cc.drill_rate = 60.0
    comp = Composer(cc)
    comp.set_spindle(1000)
    step = 0.3
    depth = 5.6
    z_seq = feed_range(-step, -depth, step)
    idx = 0
    coords = [[0, 0], [290, 0]]
    comp.move(coords[0])
    for z in z_seq:
        idx = (idx + 1) % 2
        comp.set_z(z)
        comp.feed(coords[idx])
        comp.lift()
        comp.pause(1000)
    comp.cfg.lift_z = 30
    comp.lift()
    comp.set_spindle(0)
    with open('cut_side.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
