import unittest
from composer import Composer, ComposerConfig
from transform2d import Transform2D
from feedrange import feed_range

class TestProgram(unittest.TestCase):
    def test_program_a(self):
        z_seq = feed_range(0.0, -1.0, 0.25)
        comp = Composer(ComposerConfig())
        # The program
        comp.set_spindle(1000.0)
        comp.move([-50.0, 10])
        for z in z_seq:
            comp.set_z(z)
            comp.feed([50.0, 10])
            comp.feed([50.0, -10.0])
            comp.feed([-50.0, -10.0])
            comp.feed([-50.0, 10.0]) 
        comp.move([0, 0])
        comp.set_spindle(0)
        # End of program
        res = comp.program
        expected = [
            'M3 S1000.000',
            'G1 Z3.000 F1500.000',
            'G1 X-50.000 Y10.000 F1500.000',
            'G1 Z0.000 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y10.000 F100.000',
            'G1 Z-0.250 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y10.000 F100.000',
            'G1 Z-0.500 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y10.000 F100.000',
            'G1 Z-0.750 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y10.000 F100.000',
            'G1 Z-1.000 F50.000',
            'G1 X50.000 Y10.000 F100.000',
            'G1 X50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y-10.000 F100.000',
            'G1 X-50.000 Y10.000 F100.000',
            'G1 Z3.000 F1500.000',
            'G1 X0.000 Y0.000 F1500.000',
            'M5',
        ]
        self.assertListEqual(expected, res)
        
    def test_program_b(self):
        comp = Composer(ComposerConfig())
        comp.set_z(-0.2)
        comp.move([-50.0, 20])
        comp.feed_arc([50.0, 20], [0.0, 300.0], False)
        comp.tfm = comp.tfm.flip_y()
        comp.move([-50.0, 20])
        comp.feed_arc([50.0, 20], [0.0, 300.0], False)
        res = comp.program
        expected = [
            'G1 Z3.000 F1500.000',
            'G1 X-50.000 Y20.000 F1500.000',
            'G1 Z-0.200 F50.000',
            'G3 X50.000 Y20.000 I0.000 J300.000 F100.000',
            'G1 Z3.000 F1500.000',
            'G1 X-50.000 Y-20.000 F1500.000',
            'G1 Z-0.200 F50.000',
            'G2 X50.000 Y-20.000 I0.000 J-300.000 F100.000',
        ]
        self.assertListEqual(expected, res)