from abstractcontour import AbstractContour

class ProgramA(AbstractContour):
    def __init__(self, origin):
        super().__init__(origin)

    def get_contour(self):
        cmds = [
        lambda: self.feed([50.0, 10.0]),
        lambda: self.feed([50.0, -10.0]),
        lambda: self.feed([-50.0, -10.0]),
        lambda: self.feed([50.0, 10.0]),
        ]
        return cmds

    def on_start(self):
        self.set_spindle(10000.0)
        self.move([-50.0, 10.0])

    def on_finish(self):
        self.move([0.0, 0.0])