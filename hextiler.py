# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

from geometry import Coordinates
from geometry import Hexagon
from geometry import Rectangle
from renderer import Renderer
import math

WIDTH = 15.0
HEIGHT = 10.0
SIZE_TEMP = 1.0

# This is where we'll actually do hexagon manipulation
def dummy_grid(rows, cols, size):
	origins = []
	for j in range(rows):
		for i in range(cols):
			origins.append(Coordinates(i*size, j*size))
	return origins

def make_grid(width, height, total_hexes):
	#todo
	return dummy_grid(3,4,1)

def get_centres_within_region(bottom_left, top_right, offset, size):
	centres = []
	odd = True
	current_centre = Coordinates(bottom_left.x + offset.x, bottom_left.y + offset.y)
	while current_centre.y < top_right.y:
		while current_centre.x < top_right.x + (size * math.sqrt(3) / 2):
			centres.append(Coordinates(current_centre.x, current_centre.y))
			current_centre.x += size * math.sqrt(3)

		current_centre.y += size * 1.5
		current_centre.x = bottom_left.x + offset.x
		if odd:
			odd = False
			current_centre.x -= size * math.sqrt(3) / 2
		else:
			odd = True
	return centres


hex_vertex_bundles = []
for centre in get_centres_within_region(Coordinates(0,0),
										Coordinates(WIDTH, HEIGHT),
										Coordinates(SIZE_TEMP*math.sqrt(3)/2, SIZE_TEMP*0.5),
										SIZE_TEMP):
	hex_vertex_bundles.append(Hexagon(centre, SIZE_TEMP, "VERTICAL").get_vertices())


bounding = Rectangle(Coordinates(0, 0), Coordinates(WIDTH, HEIGHT))

R = Renderer()

R.render(bounding.get_vertices(), hex_vertex_bundles)
