from gcodeprogram import GCodeProgram

class ProgramA(GCodeProgram):
    def __init__(self, origin):
        super().__init__(origin)

    def contour_forward(self):
        self.feed([50.0, 10.0])
        self.feed([50.0, -10.0])
        self.feed([-50.0, -10.0])

    def contour_backward(self):
        self.feed([50.0, -10.0])
        self.feed([50.0, 10.0])
        self.feed([-50.0, 10.0])

    def on_start(self):
        self.move([-50.0, 10.0])

    def on_finish(self):
        self.move([0.0, 0.0])

    def is_bidirectional(self):
        return True