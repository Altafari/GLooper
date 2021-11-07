from abc import ABC, abstractmethod
from transform2d import Transform2D

class AbstractContour(ABC):
    @abstractmethod
    def __init__(self, origin):
        self.origin = origin      # 2-D origin of the part
        self.tfm = None           # Current transform, top of the transform stack
        self.cmp = None           # Current program composer instance 

    @abstractmethod
    def get_contour(self):
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_finish(self):
        pass    

    def proces_contour(self, comp, z_seq):
        self.comp = comp
        self.tfm = self.origin
        self.comp.set_z(z_seq[0])
        self.on_start()        
        self.process_loop(z_seq)
        self.on_finish()

    def process_loop(self, z_seq):
        cmds = self.get_contour()
        for z in z_seq:
            self.tfm = self.origin
            self.comp.set_z(z)
            for cmd in cmds:
                cmd()

    def set_transform(self, tfm):
        self.tfm = self.origin.compose(tfm)

    def add_transform(self, tfm):
        self.tfm = self.tfm.compose(tfm)

    def feed(self, tgt):
        tgt_t = self.tfm.apply(tgt)
        self.comp.feed(tgt_t)

    def feed_arc(self, tgt, ctr, is_cw):
        tgt_t = self.tfm.apply(tgt)
        ctr_t = self.tfm.apply(ctr)
        is_cw = is_cw ^ self.tfm.is_mirroring()
        self.comp.feed_arc(tgt_t, ctr_t, is_cw)

    def move(self, tgt):
        tgt_t = self.tfm.apply(tgt)
        self.comp.move(tgt_t)

    def set_spindle(self, speed):
        self.comp.set_spindle(speed)