import unittest
from composer import Composer, ComposerConfig
from sampleprograms import ProgramA
from transform2d import Transform2D

class TestProgram(unittest.TestCase):
    def test_program_a(self):
        prg = ProgramA(Transform2D())
        z_seq = [0, -0.1, -0.2, -0.3]
        comp = Composer(ComposerConfig())
        prg.proces_contour(comp, z_seq)
        res = comp.program
        expected = [
            'M3 S10000.000',
            'G0 Z3.000 F300.000',
            'G0 X-50.000 Y10.000 F300.000',
            'G1 Z0.000 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 Z-0.100 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 Z-0.200 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 Z-0.300 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X50.000 Y10.000 F100.000',
            'G0 Z3.000 F300.000',
            'G0 X0.000 Y0.000 F300.000',
        ]
        self.assertListEqual(expected, res)