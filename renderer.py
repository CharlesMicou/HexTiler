# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

class Renderer:
	def __init__(self):
		print "Renderer init goes here please"

	def test_render(self, points):
		fig, ax = plt.subplots()
		plot_polygon(points, ax)
		#ax.grid()
		ax.axis('equal')
		plt.show()



def plot_polygon(vertices, ax):
	Path = mpath.Path
	path_data = [(Path.MOVETO, (vertices[0].x, vertices[0].y))]
	for vertex in vertices:
		path_data.append((Path.LINETO, (vertex.x, vertex.y)))
	path_data.append((Path.CLOSEPOLY, (vertices[0].x, vertices[0].y)))
	codes, verts = zip(*path_data)
	path = mpath.Path(verts, codes)
	patch = mpatches.PathPatch(path, facecolor='b', alpha=0.4)
	ax.add_patch(patch)