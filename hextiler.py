# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

from hexagon import Coordinates
from hexagon import Hexagon

# This is where we'll actually do hexagon manipulation
a = Coordinates(1, 2)

b = Hexagon(a, 2, "VERTICAL")

c = b.get_vertices()

print c