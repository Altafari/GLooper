from abc import ABC, abstractmethod


class GCodeProgram(ABC):
    @abstractmethod
    def __init__(self, origin):
        self.origin = origin
        self.transform = []
        self.program = []
        self.feed_rate = 100
        self.drill_rate = 50
        self.move_rate = 300
        self.lift_height = 3
        pass

    def feed(self):
        pass

    def origin(self, origin):
        if origin is not None:
            self.origin = origin
        return self.origin

    def move(self, tgt):
        pass

    def lift(self):
        pass

    def drill(self):
        pass

    def hop(self, tgt):
        self.lift()
        self.move(tgt)
        self.drill()

    def cut_line(self):
        pass

    def cut_arc(self):
        pass

    def push_transform(self, tfm):
        self.transform.append(tfm)

    def pop_transform(self):
        self.transform = self.transform[:-1]

    def set_transform(self, tfm):
        self.transform = tfm