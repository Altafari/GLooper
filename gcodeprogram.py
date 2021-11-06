from abc import ABC, abstractmethod
from transform2d import Transform2D

class GCodeProgram(ABC):
    @abstractmethod
    def __init__(self, origin):
        self.origin = origin                        # 2-D origin of the part
        self.tfm = Transform2D().translate(origin)  # Current transform, top of the transform stack
        self.transform = [self.tfm]                 # Transform stack
        self.program = []                           # G-code strings
        self.feed_rate = 100.0
        self.drill_rate = 50.0
        self.move_rate = 300.0
        self.lift_height = 3.0
        self.is_lifted = False                      # Indicates mill state
        self.float_fmt = "%.3f"
        self.current_z = 0.0

    @abstractmethod
    def contour_forward(self):
        pass

    @abstractmethod    
    def contour_backward(self):
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_finish(self):
        pass

    @abstractmethod
    def is_bidirectional(self):
        pass

    def proces_contour(self, z_seq):
        contours = [self.contour_forward, self.contour_backward]
        self.on_start()
        for i, z in enumerate(z_seq):
            self.current_z = z
            self.drill()
            contours[i % 2]()
        self.on_finish()

    def feed(self, tgt):
        if self.is_lifted:
            self.drill()
        cmd_str = self.float_fmt.join(["G1 X", " Y", " F", ""])
        dest = self.tfm.apply(tgt)
        self.program.append(cmd_str % (dest[0], dest[1], self.feed_rate))

    def move(self, tgt):
        if not self.is_lifted:
            self.lift()
        cmd_str = self.float_fmt.join(["G0 X", " Y", " F", ""])
        dest = self.tfm.apply(tgt)
        self.program.append(cmd_str % (dest[0], dest[1], self.move_rate))

    def lift(self):
        cmd_str = self.float_fmt.join(["G0 Z", " F", ""]) 
        self.program.append(cmd_str % (self.lift_height, self.move_rate))
        self.is_lifted = True

    def drill(self):
        cmd_str = self.float_fmt.join(["G1 Z", " F", ""])
        self.program.append(cmd_str % (self.current_z, self.drill_rate))
        self.is_lifted = False

    def feed_arc(self, tgt, ctr, is_cw):
        dest = self.tfm.apply(tgt)
        center = self.tfm.apply(ctr)
        is_cw = is_cw ^ self.tfm.is_mirroring()
        if is_cw:
            cmd_str = "G2 "
        else:
            cmd_str = "G3 "
        cmd_str = cmd_str + self.float_fmt.join(["X", " Y", " I", " J", " F", ""])
        slef.program.append(cmd_str % (dest[0], dest[1], center[0], center[1], self.feed_rate))

    def push_transform(self, tfm):
        self.transform.append(tfm.compose(self.tfm))
        self.tfm = self.transform[-1]

    def pop_transform(self):
        self.transform = self.transform[:-1]
        self.tfm = self.transform[-1]

    def set_transform(self, tfm):
        self.transform = [tfm]
        self.tfm = tfm