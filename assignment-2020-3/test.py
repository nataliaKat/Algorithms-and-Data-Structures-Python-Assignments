from pprint import pprint

def read_boundary_from_file(filename):  
    boundaries = set()
    with open(filename) as bounds:
        for line in bounds:
            items = line.split()
            u = (float(items[0]), float(items[1]))
            v = (float(items[2]), float(items[3]))
            boundaries.add((u, v))
    return boundaries

a = read_boundary_from_file("rectangle.txt")
