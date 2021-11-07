import unittest
import numpy as np
from transform2d import Transform2D

class TestTransform2D(unittest.TestCase):

    def test_default_ctr(self):
        tfm = Transform2D()
        v = [5.6, 3.8]
        res = tfm.apply(v).tolist()
        self.assertListEqual(v, res)

    def test_apply(self):
        tfm = Transform2D().translate([2.0, 5.0])
        v = [2.0, 1.0]
        expected = [4.0, 6.0]
        res = tfm.apply(v).tolist()
        self.assertListEqual(expected, res)
        
    def test_compose(self):
        tfm_a = Transform2D().rotate(90)
        tfm_b = Transform2D().translate([2.0, 3.0])
        tfm_c = Transform2D().rotate(-90)
        tfm_d = Transform2D().translate([1.0, -1.0])
        tfm = tfm_a
        for t in [tfm_b, tfm_c, tfm_d]:
            tfm = tfm.compose(t)
        v = [0.0, 0.0]
        res = tfm.apply(v).tolist()
        expected = [-2.0, 1.0]
        self.assertListEqual(expected, res)

    def test_flip_x(self):
        tfm = Transform2D().flip_x().translate([2.0, 3.0])
        res = tfm.apply([0.0, 0.0]).tolist()
        expected = [-2.0, 3.0]
        self.assertListEqual(expected, res)

    def test_flip_y(self):
        tfm = Transform2D().flip_y().translate([2.0, 3.0])
        res = tfm.apply([0.0, 0.0]).tolist()
        expected = [2.0, -3.0]
        self.assertListEqual(expected, res)

    def test_scale(self):
        tfm = Transform2D().scale([0.5, 2]).translate([2.0, 3.0])
        res = tfm.apply([0.0, 0.0]).tolist()
        expected = [1.0, 6.0]
        self.assertListEqual(expected, res)

    def test_is_mirroring(self):
        tfm_a = Transform2D().rotate(180)
        tfm_b = tfm_a.flip_x()
        tfm_c = tfm_b.flip_y()
        self.assertFalse(tfm_a.is_mirroring())
        self.assertTrue(tfm_b.is_mirroring())
        self.assertFalse(tfm_c.is_mirroring())