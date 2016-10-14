# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

from hexagon import Coordinates
from hexagon import Hexagon
from renderer import Renderer
# This is where we'll actually do hexagon manipulation
a = Coordinates(1, 2)
b = Hexagon(a, 2, "HORIZONTAL")
c = b.get_vertices()

R = Renderer()

R.test_render(c)