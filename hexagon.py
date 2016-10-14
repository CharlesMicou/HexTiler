# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

import math

# Utility for managing hexagons
class Hexagon:
	def __init__(self, centre_coordinates, edge_length, orientation):
		self.coordinates = centre_coordinates
		self.edge_length = edge_length
		self.orientation = orientation
		#Validate orientation
		if (orientation != "VERTICAL") and (orientation != "HORIZONTAL"):
			print "hex orientation was not specified correctly (\"HORIZONTAL\" or \"VERTICAL\")"

	def get_vertices(self):
		vertices = []
		for vertex in range(0,6):
			if self.orientation == "HORIZONTAL":
				angle = vertex * math.pi / 3
			if self.orientation == "VERTICAL":
				angle = vertex * math.pi / 3 + math.pi / 6
			next_vertex = Coordinates(
				self.coordinates.x + math.cos(angle) * self.edge_length, 
				self.coordinates.y + math.sin(angle) * self.edge_length)
			vertices.append(next_vertex)
		return vertices

class Coordinates:
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def __str__(self):
		return "Coordinates (" + str(self.x) + ", " + str(self.y) + ")"

	def __repr__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"