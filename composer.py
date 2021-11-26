from transform2d import Transform2D

class ComposerConfig:
    def __init__(self):
        self.feed_rate = 100.0
        self.drill_rate = 50.0
        self.lift_z = 3.0

class Composer:
    def __init__(self, config):
        self.cfg = config
        self.program = []          # G-code strings
        self.is_lifted = False
        self.is_drilled = False
        self.float_fmt = "%.3f"
        self.current_z = None
        self.tfm = Transform2D()

    def set_z(self, z):
        if not self.current_z or z != self.current_z:
            self.current_z = z
            self.is_drilled = False

    def set_spindle(self, speed):
        if speed > 0.0:
            cmd_str = "M3 S" + self.float_fmt
            self.program.append(cmd_str % speed)
        else:
            self.program.append("M5")

    def feed(self, tgt):
        if not self.is_drilled:
            self.drill()
        cmd_str = self.float_fmt.join(["G1 X", " Y", " F", ""])
        params = self._transform(tgt)
        self.program.append(cmd_str % (*params, self.cfg.feed_rate))

    def feed_arc(self, tgt, ctr_off, is_cw):
        if not self.is_drilled:
            self.drill()
        if is_cw ^ self.tfm.is_mirroring():
            cmd_str = "G2 "
        else:
            cmd_str = "G3 "
        cmd_str = cmd_str + self.float_fmt.join(["X", " Y", " I", " J", " F", ""])
        params = self._transform(tgt, ctr_off)
        self.program.append(cmd_str % (*params, self.cfg.feed_rate))

    def move(self, tgt):
        if not self.is_lifted:
            self.lift()
        cmd_str = self.float_fmt.join(["G0 X", " Y",  ""])
        params = self._transform(tgt)
        self.program.append(cmd_str % params)

    def lift(self):
        cmd_str = self.float_fmt.join(["G0 Z", ""]) 
        self.program.append(cmd_str % self.cfg.lift_z)
        self.is_lifted = True
        self.is_drilled = False

    def drill(self):
        cmd_str = self.float_fmt.join(["G1 Z", " F", ""])
        self.program.append(cmd_str % (self.current_z, self.cfg.drill_rate))
        self.is_lifted = False
        self.is_drilled = True

    def set_tfm(self, tfm):
        self.tfm = tfm

    def _transform(self, *args):
        func = [self.tfm.apply, self.tfm.affine]
        vect = (f(v) for f, v in zip(func, args))
        return tuple(x for v in vect for x in v)
    