import math
import argparse
import random
import sys

def find_tangent_circle(cm, cn, r):
    dx = cn[0] - cm[0]
    dy = cn[1] - cm[1]
    d = math.sqrt(dx ** 2 + dy ** 2)
    r1 = cm[2] + r
    r2 = cn[2] + r
    l = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d ** 2)
    e = math.sqrt(r1 ** 2 / d ** 2 - l ** 2)
    c = (round(cm[0] + l * dx - e * dy, 2),
         round(cm[1] + l * dy + e * dx, 2), r)
    return c

def deep_copy(a, b):
    for k in a.keys():
        b[k] = []
        for x in a[k]:
            b[k].append(x)
    return b

def get_previous(element):
    return list(battlefront[element])[2]

def get_next(element):
    return list(battlefront[element])[3]

def update_previous(element, value):
    battlefront[element][2] = value

def update_next(element, value):
    battlefront[element][3] = value

def find_circle_distance_from_00(c):
    return round(math.sqrt(c[0] ** 2 + c[1] ** 2), 2)

def get_circle_nearest_to_beginning():
    sorted_keys = sorted(battlefront, key=lambda e:list(battlefront[e])[0])
    return min(sorted_keys, key=lambda k: list(battlefront[k])[1] if k not in dead else sys.maxsize) 

def do_circles_intersect(c1, c2):
    dist = round(math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2), 2)
    if dist < c1[2] + c2[2]:
        return True
    return False

def delete_from_battlefront(key):
    previous = get_previous(key)
    next = get_next(key)
    del battlefront[key]
    update_next(previous, next)
    update_previous(next, previous)

def get_intersecting_circle(ci, cm, cn):
    middle = len(battlefront) // 2
    inters = 0
    a = get_next(cn)
    b = get_previous(cm)
    for i in range(middle):
        if do_circles_intersect(a, ci):
            return (a, 1)
        elif do_circles_intersect(b, ci):
            return (b, 2)
        a = get_next(a)
        b = get_previous(b)
    return 0

def get_circle_dist_from_straight_line(c, u, v):
    l2 = (u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2
    if l2 == 0:
        return round(math.sqrt((u[0] - c[0]) ** 2 + (u[1] - c[1]) ** 2), 2)
    t = ((c[0] - u[0]) * (v[0] - u[0]) + (c[1] - u[1]) * (v[1] - u[1])) / l2
    t = max(0, min(1, t))
    px = u[0] + t * (v[0] - u[0])
    py = u[1] + t * (v[1] - u[1])
    return round(math.sqrt((px - c[0]) ** 2 + (py - c[1]) ** 2), 2)

def does_circle_intersect_with_bounds(c):
    for str_line in bounds:
        if get_circle_dist_from_straight_line(c, str_line[0], str_line[1]) < c[2]:
            return True
    return False

def step5(ci, cm, cn, cj):
    cj, nearer = cj[0], cj[1]
    if nearer == 2:
        a = get_next(cj)
        while a != cn:
            x = get_next(a)
            delete_from_battlefront(a)
            a = x
        return 1
    a = get_next(cm)
    while a != cj:
        x = get_next(a)
        delete_from_battlefront(a)
        a = x
    return 2

def read_boundary_from_file(filename):  
    boundaries = []
    with open(filename) as bounds:
        for line in bounds:
            items = line.split()
            u = (float(items[0]), float(items[1]))
            v = (float(items[2]), float(items[3]))
            boundaries.append((u, v))
    return boundaries

def write_in_file(circles, filename, bounds = []):
    f = open(filename, 'w')
    for c in circles:
        x = "{:.2f}".format(c[0])
        y = "{:.2f}".format(c[1])
        line = x + ' ' + y + ' ' + str(c[2]) + '\n'
        f.write(line)
    if args.b:
        for l in bounds:
            line = "{} {} {} {}\n".format(l[0][0], l[0][1], l[1][0], l[1][1])
            f.write(line)
            line = ""
    f.close()

def add_to_battlefront(ci, cm, cn):
    global counter
    counter += 1
    battlefront[ci] = [counter, find_circle_distance_from_00(ci), cm, cn]
    update_previous(cn, ci)
    update_next(cm, ci)

def are_all_dead():
    for k in battlefront.keys():
        if k not in dead:
            return False
    return True

def main_alg(r, update_history=False):
    cm = get_circle_nearest_to_beginning()
    cm_first = cm
    cn = get_next(cm)
    ci = find_tangent_circle(cm, cn, r)
    inters = get_intersecting_circle(ci, cm, cn)
    c = 0
    while inters != 0:
        temp = step5(ci, cm, cn, inters)
        if temp == 1:
            cm = inters[0]
        else:
            cn = inters[0]
        ci = find_tangent_circle(cm, cn, r)
        inters = get_intersecting_circle(ci, cm, cn)
    return (ci, cm, cn, cm_first)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--items", type=int,
                    help="number of circles to be created")
parser.add_argument("-r", "--radius", type=int, help="radius of all circles")
parser.add_argument("-s", "--seed", type=float, help="seed of random function")
parser.add_argument("--min_radius", type=int,
                    help="minimum radius, combined with --max_radius")
parser.add_argument("--max_radius", type=int,
                    help="maximum radius, combined with --min_radius")
parser.add_argument("-b", "--b", help="give boundaries as x1 y1 x2 y2")
parser.add_argument("output_file", help="file to store results")

args = parser.parse_args()

global counter
counter = 2

if args.radius:
    r = r1 = r2 = args.radius
else:
    random.seed(args.seed)
    lower, upper = args.min_radius, args.max_radius
    r1 = random.randint(lower, upper)
    r2 = random.randint(lower, upper)

c1 = (0.00, 0.00, r1)
c2 = (r1 + r2, 0.00, r2)
battlefront = {c1: [1, find_circle_distance_from_00(c1), c2, c2],
            c2: [2, find_circle_distance_from_00(c2), c1, c1]
            }

circles = [c1, c2]
dead = set()

if args.items and args.b:
    history = []
    bounds = read_boundary_from_file(args.b)
    radius_not_used = False
    while counter < args.items and not are_all_dead():
        if not args.radius and not radius_not_used:
            r = random.randint(lower, upper)
        radius_not_used = True
        old_battle = {}
        deep_copy(battlefront, old_battle)
        result = main_alg(r, True)
        if does_circle_intersect_with_bounds(result[0]):
            battlefront = old_battle
            old_history = {}
            dead.add(result[3])
        else:
            circles.append(result[0])
            add_to_battlefront(result[0], result[1], result[2])
            radius_not_used = False
            dead.clear()

elif args.b:
    history = []
    bounds = read_boundary_from_file(args.b)
    radius_not_used = False
    while not are_all_dead():
        if not args.radius and not radius_not_used:
            r = random.randint(lower, upper)
        radius_not_used = True
        old_battle = {}
        deep_copy(battlefront, old_battle)
        result = main_alg(r, True)
        if does_circle_intersect_with_bounds(result[0]):
            battlefront = old_battle
            old_history = {}
            dead.add(result[3])
        else:
            circles.append(result[0])
            add_to_battlefront(result[0], result[1], result[2])
            radius_not_used = False
            dead.clear()

else:
    bounds = []
    while len(circles) < args.items:
        if not args.radius:
            r = random.randint(lower, upper)
        result = main_alg(r)
        circles.append(result[0])
        add_to_battlefront(result[0], result[1], result[2])

print(counter)
write_in_file(circles, args.output_file, bounds)
