# Created by Charlie Micou on 14/10/2016
# HexTiler project
# ======================================

from geometry import Coordinates
from geometry import Hexagon
from geometry import Rectangle
from renderer import Renderer
import math
import sys

if len(sys.argv) != 4:
	print "Usage is WIDTH HEIGHT HEXES"
	sys.exit()

WIDTH = float(sys.argv[1])
HEIGHT = float(sys.argv[2])
MAX_HEXES = int(sys.argv[3])

def get_centres_within_region(bottom_left, top_right, offset, size):
	centres = []
	odd = True
	current_centre = Coordinates(bottom_left.x + offset.x, bottom_left.y + offset.y)
	#todo fix these bounds
	while current_centre.y < top_right.y + size - size/1000:
		while current_centre.x < top_right.x + size*math.sqrt(3)/2 - size/1000 :
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

def solve_quadratic(a, b, c):
    if b**2 - 4*a*c < 0:
        print "Complex solution to quadratic, you don't want this"
        return
    little_root = (-b - math.sqrt(b**2 - 4*a*c))/(2.0*a)
    big_root = (-b + math.sqrt(b**2 - 4*a*c))/(2.0*a)
    return [little_root, big_root]

def smallest_positive(a):
    current_candidate = sys.maxint
    for element in a:
        if element > 0 and element < current_candidate:
            current_candidate = element
    return current_candidate

def solve(W, H, N):
	vertical_solution = solve_vertical(W, H, N)
	horizontal_solution = solve_vertical(H, W, N)
	if vertical_solution > horizontal_solution:
		return (horizontal_solution, "HORIZONTAL")
	else:
		return (vertical_solution, "VERTICAL")


def solve_vertical(W, H, N):

	if N < 2:
		# Just one hexagon, this will result in a divide by zero
		# We need a rectangle enclosed by one pointy hexagon
		d_width = W / math.sqrt(3)
		d_height = H
		return max(d_width, d_height)

	# Solve continuous via a quadratic
	a = 3*N + 1
	b = W * (2/math.sqrt(3) - math.sqrt(3)) - H
	c = -2*W*H/math.sqrt(3)
	x = smallest_positive(solve_quadratic(a,b,c))

	# Get alpha and beta
	alpha = math.floor(W/(math.sqrt(3)*x)) + 1
	beta = math.floor((H/x - 1)/3)

	# Try restricting by width:
	if (math.sqrt(3)*math.floor((N - 3*beta - 1)/(2*beta + 1))) != 0:
		d_width = W/(math.sqrt(3)*math.floor((N - 3*beta - 1)/(2*beta + 1)))
	else:
		d_width = W / math.sqrt(3)

	if d_width <= 0:
		# degenerate case
		d_width = W / math.sqrt(3)
	else:
		current_N = len(get_centres_within_region(Coordinates(0,0),
						Coordinates(WIDTH, HEIGHT),
						Coordinates(d_width*math.sqrt(3)/2, d_width*0.5),
						d_width))

		if current_N > N:
			# we wanted too many, decrease number of columns until we are ok
			trial_cols = int(math.ceil(W/(d_width*math.sqrt(3))))
			while current_N >= N:
				trial_cols -= 1
				if trial_cols < 1:
					# prevent getting stuck in degenerate cases
					d_width = sys.maxint
					break
				d_width = W/(math.sqrt(3)*trial_cols)
				current_N = len(get_centres_within_region(Coordinates(0,0),
								Coordinates(WIDTH, HEIGHT),
								Coordinates(d_width*math.sqrt(3)/2, d_width*0.5),
								d_width))
		else:
			# check for solutions that might exist with smaller d
			trial_cols = int(math.ceil(W/(d_width*math.sqrt(3))))
			next_N = current_N
			next_d_width = d_width
			while next_N <= N:
				d_width = next_d_width
				trial_cols += 1
				next_d_width = W/(math.sqrt(3)*trial_cols)
				next_N = len(get_centres_within_region(Coordinates(0,0),
								Coordinates(WIDTH, HEIGHT),
								Coordinates(next_d_width*math.sqrt(3)/2, next_d_width*0.5),
								next_d_width))

	# Try restricting by height
	d_height = H/(math.floor(N/(2*alpha+1))*3+1)

	if d_height < 0:
		#degenerate case
		d_height = H
	# Shrink/grow d so that we don't need too many hexes:
	current_N = len(get_centres_within_region(Coordinates(0,0),
					Coordinates(WIDTH, HEIGHT),
					Coordinates(d_height*math.sqrt(3)/2, d_height*0.5),
					d_height))

	if current_N > N:
		# we wanted too many, decrease number of columns until we are ok
		trial_rows = int(math.ceil(H/(1.5*d_height) - 2.0/3.0))
		while current_N >= N:
			trial_rows -= 1
			if trial_rows < 1:
				d_height = sys.maxint
				# prevent getting stuck in degenerate cases
				break
			d_height = H/(1+1.5*(trial_rows-1))
			current_N = len(get_centres_within_region(Coordinates(0,0),
							Coordinates(WIDTH, HEIGHT),
							Coordinates(d_height*math.sqrt(3)/2, d_height*0.5),
							d_height))
	else:
		# check for solutions that might exist with smaller d
		trial_rows = int(math.ceil(H/(1.5*d_height) - 2.0/3.0))
		next_N = current_N
		next_d_height = d_height
		while next_N <= N:
			d_height = next_d_height
			trial_rows += 1
			next_d_height = H/(1+1.5*(trial_rows-1))
			next_N = len(get_centres_within_region(Coordinates(0,0),
							Coordinates(WIDTH, HEIGHT),
							Coordinates(next_d_height*math.sqrt(3)/2, next_d_height*0.5),
							next_d_height))

	return min([d_width, d_height])


solution = solve(WIDTH, HEIGHT, MAX_HEXES)

if solution[1] == "HORIZONTAL":
	centres = get_centres_within_region(Coordinates(0,0),
										Coordinates(HEIGHT, WIDTH),
										Coordinates(solution[0]*math.sqrt(3)/2, solution[0]*0.5),
										solution[0])
	for centre in centres:
		temp = centre.x
		centre.x = centre.y
		centre.y = temp

else:
	centres = get_centres_within_region(Coordinates(0,0),
										Coordinates(WIDTH, HEIGHT),
										Coordinates(solution[0]*math.sqrt(3)/2, solution[0]*0.5),
										solution[0])

# Centre the hexagons for symmetry by finding a bounding Rectangle
min_x = sys.maxint
max_x = -sys.maxint
min_y = sys.maxint
max_y = -sys.maxint
for centre in centres:
	min_x = min(centre.x, min_x)
	max_x = max(centre.x, max_x)
	min_y = min(centre.y, min_y)
	max_y = max(centre.y, max_y)
hexagon_centre_of_mass = Coordinates((max_x+min_x)/2.0, (max_y+min_y)/2.0)
adjustment = Coordinates(WIDTH / 2 - hexagon_centre_of_mass.x, HEIGHT / 2 - hexagon_centre_of_mass.y)
for centre in centres:
	centre.x += adjustment.x
	centre.y += adjustment.y

# Result
print "Used " + str(len(centres)) + " of " + str(MAX_HEXES) + " hexes. Next break-point at [unimplemented] total hexes."

# Draw the hexes
hex_vertex_bundles = []
for centre in centres:
	hex_vertex_bundles.append(Hexagon(centre, solution[0], solution[1]).get_vertices())
bounding = Rectangle(Coordinates(0, 0), Coordinates(WIDTH, HEIGHT))
R = Renderer()
R.render(bounding.get_vertices(), hex_vertex_bundles)
