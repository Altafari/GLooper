from math import sqrt

from transform2d import Transform2D

class PContext:
    def __init__(self, composer, z_seq, mill_rad, is_cutout):
        self.comp = composer
        self.z_seq = z_seq
        self.mill_rad = mill_rad
        self.is_cutout = is_cutout
    
    def get_offset(self):
        return self.mill_rad if self.is_cutout else -self.mill_rad


def cut_rectangle(cont, width, height, origin):
    comp = cont.comp
    offset = cont.get_offset()
    corners = __compute_corners(offset, width, height)
    comp.set_tfm(origin)
    comp.move(corners[-1])
    for z in cont.z_seq:
        comp.set_z(z)
        for corner in corners:
            comp.feed(corner)

def cut_slot(cont, width, height, origin):
    if not cont.is_cutout:
        raise Exception('Slot must be a cutout')
    comp = cont.comp    
    offset = cont.get_offset()
    corners = __compute_corners(offset, width, height)
    cutouts = __compute_cutouts(cont.mill_rad)
    comp.set_tfm(origin)
    comp.move(corners[-1])
    for z in cont.z_seq:
        comp.set_z(z)
        for corner, cutout in zip(corners, cutouts):
            comp.feed(corner)
            comp.feed([corner[0] + cutout[0], corner[1] + cutout[1]])
            comp.feed(corner)

def cut_circle(cont, diameter, center):
    comp = cont.comp
    offset = cont.get_offset()
    radius = (0.5 * diameter) - offset
    comp.set_tfm(center)
    start = [radius, 0]
    comp.move(start)
    for z in cont.z_seq:
        comp.set_z(z)
        comp.feed_arc(start, [-radius, 0], True)

def __compute_corners(offset, width, height):
    y_max = height - offset
    x_max = width - offset
    return [[offset, y_max], [x_max, y_max], [x_max, offset], [offset, offset]]

def __compute_cutouts(mill_rad):
    delta = mill_rad * (1.0 / sqrt(2.0) - 1)
    dvect = [delta, delta]
    cutouts = []
    rtfm = Transform2D().rotate(-90)
    for _ in range(4):
        dvect = rtfm.apply(dvect).tolist()
        cutouts.append(dvect)
    return cutouts