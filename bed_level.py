from xml.etree import ElementInclude
from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range
from math import sqrt

class LevelGCodeGenerator:
    def __init__(self, composer, width, height):
        self.comp = composer
        self.width = width
        self.height = height
        self.finish = True
        self.depth = 0

    def render_program(self):
        comp = self.comp        
        comp.move([0, 0])
        y = self.height
        if self.finish:
            comp.set_z(self.depth-0.05)
            for x in feed_range(0.5, self.width, 1):                
                comp.move([x, 0])
                comp.feed([x, y])
        else:
            comp.set_z(self.depth)
            for x in feed_range(0, self.width, 1):
                comp.feed([x, y])
                if y != 0:
                    y = 0
                else:
                    y = self.height
                comp.feed([x, y])


if __name__ == '__main__':
    cc = ComposerConfig()
    cc.feed_rate = 1000.0
    cc.drill_rate = 500.0
    cc.lift_z = 0.5
    comp = Composer(cc)
    comp.set_spindle(1000)
    p = LevelGCodeGenerator(comp, 300, 180)
    p.render_program()
    comp.lift()
    comp.set_spindle(0)
    with open('level.nc', 'w+') as f:
        f.write('\n'.join(comp.program))
