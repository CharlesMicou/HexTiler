# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

from geometry import Coordinates
from geometry import Hexagon
from geometry import Rectangle
from renderer import Renderer
# This is where we'll actually do hexagon manipulation

hex_a = Hexagon(Coordinates(1, 2), 2, "HORIZONTAL")
hex_b = Hexagon(Coordinates(-1, 4), 1, "VERTICAL")

bounding = Rectangle(Coordinates(0, 0), Coordinates(3, 2))

R = Renderer()

R.render(bounding.get_vertices(), [hex_a.get_vertices(), hex_b.get_vertices()])