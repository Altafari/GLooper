from math import cos, sin
import numpy as np

class Transform2D:
    def __init__(self, *args):
        if len(args) > 0:
            self.tfm = args[0]
        else:
            self.tfm = np.eye(3)

    def __repr__(self):
        return repr(self.tfm)

    def apply(self, x):
        return np.dot(self.tfm, np.array(x + [1.0]))[0:2]

    def compose(self, tfm):
        if isinstance(tfm, type(self)):
            tfm = tfm.tfm
        return Transform2D(np.matmul(self.tfm, tfm))
    
    def translate(self, v):
        return self.compose(np.array([(1.0, 0.0, v[0]), (0.0, 1.0, v[1]), (0.0, 0.0, 1.0)]))

    def rotate(self, angle):
        arad = np.deg2rad(angle)
        s, c = sin(arad), cos(arad)
        return self.compose(np.array([(c, -s, 0.0), (s, c, 0.0), (0.0, 0.0, 1.0)]))

    def flip_x(self):
        return self.compose(np.array([(-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]))

    def flip_y(self):
        return self.compose(np.array([(1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0)]))
    
    def scale(self, v):
        return self.compose(np.array([(v[0], 0.0, 0.0), (0.0, v[1], 0.0), (0.0, 0.0, 1.0)]))

    def is_mirroring(self):
        return np.linalg.det(self.tfm[0:2, 0:2]) < 0.0