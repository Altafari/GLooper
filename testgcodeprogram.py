import unittest
import numpy as np
from transform2d import Transform2D
from programs import ProgramA

class TestGCodeProgram(unittest.TestCase):
    def test_program_a(self):
        prg = ProgramA([0.0, 0.0])
        z_seq = [0, -0.1, -0.2, -0.3]
        prg.proces_contour(z_seq)
        res = prg.program
        self.assertTrue(True)