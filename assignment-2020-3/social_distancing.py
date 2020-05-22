import math
from pprint import pprint
import argparse
import random


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


def get_previous(d, element):
    return list(d[element])[0]


def get_next(d, element):
    return list(d[element])[1]


def update_previous(battlefront, element, value):
    battlefront[element][0] = value


def update_next(battlefront, element, value):
    battlefront[element][1] = value


def find_circle_distance_from_00(c):
    return round(math.sqrt(c[0] ** 2 + c[1] ** 2), 2)


def get_circle_nearest_to_beginning(circles):
    return min(circles, key=lambda k: k[1])


def do_circles_intersect(c1, c2):
    dist = round(math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2), 2)
    if dist < c1[2] + c2[2]:
        return True
    return False


def delete_from_battlefront_dict(battlefront, key):
    previous = get_previous(battlefront, key)
    next = get_next(battlefront, key)
    del battlefront[key]
    update_next(battlefront, previous, next)
    update_previous(battlefront, next, previous)
    return battlefront


def get_intersecting_circle(battlefront, ci, cm, cn):
    inters_circles = []
    a = get_next(battlefront, cn)
    while a != cm:
        if do_circles_intersect(ci, a):
            inters_circles.append(a)
        a = get_next(battlefront, a)
    if inters_circles:
        cj_first = inters_circles[0]
        cj_last = inters_circles[-1]
        
        bnjf, bmjl = 0, 0
        a = get_next(battlefront, cn)
        while a != cj_first:
            bnjf += 1
            a = get_next(battlefront, a)
        a = get_previous(battlefront, cm)
        while a != cj_last:
            bmjl += 1
            a = get_previous(battlefront, a)
        if bmjl < bnjf:
            return (cj_last, 2)
        return (cj_first, 1)
    return 0

def step5(battlefront, ci, cm, cn, cj):
    cj, nearer = cj[0], cj[1]
    if nearer == 2:
        a = get_next(battlefront, cj)
        while a != cn:
            x = get_next(battlefront, a)
            battlefront = delete_from_battlefront_dict(battlefront, a)
            for k in battlefront_in_order:
                if k[0] == a:
                    battlefront_in_order.remove(k)
                    break
            a = x
        return 1
    a = get_next(battlefront, cm)
    while a != cj:
        x = get_next(battlefront, a)
        battlefront = delete_from_battlefront_dict(battlefront, a)
        for k in battlefront_in_order:
            if k[0] == a:
                battlefront_in_order.remove(k)
                break
        a = x
    return 2


def write_in_file(circles, filename):
    f = open(filename, 'w')
    for c in circles:
        x = "{:.2f}".format(c[0])
        y = "{:.2f}".format(c[1])
        line = x + ' ' + y + ' ' + str(c[2]) + '\n'
        f.write(line)
    f.close()


def main_alg(r):
    cm = get_circle_nearest_to_beginning(battlefront_in_order)[0]
    cn = get_next(battlefront, cm)
    ci = find_tangent_circle(cm, cn, r)
    inters = get_intersecting_circle(battlefront, ci, cm, cn)
    while inters != 0:
        temp = step5(battlefront, ci, cm, cn, inters)
        if temp == 1:
            cm = inters[0]
        else:
            cn = inters[0]
        ci = find_tangent_circle(cm, cn, r)
        inters = get_intersecting_circle(battlefront, ci, cm, cn)

    battlefront[ci] = [cm, cn]
    update_previous(battlefront, cn, ci)
    update_next(battlefront, cm, ci)
    battlefront_in_order.append((ci, find_circle_distance_from_00(ci)))
    circles.append(ci)

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

if args.radius:
    r = r1 = r2 = args.radius
else:
    random.seed(args.seed)
    lower, upper = args.min_radius, args.max_radius
    r1 = random.randint(lower, upper)
    r2 = random.randint(lower, upper)

c1 = (0.00, 0.00, r1)
c2 = (r1 + r2, 0.00, r2)
battlefront = {c1: [c2, c2],
               c2: [c1, c1]
               }
battlefront_in_order = [(c1, find_circle_distance_from_00(
    c1)), (c2, find_circle_distance_from_00(c2))]
circles = [c1, c2]

while len(circles) < args.items:
    if not args.radius:
        r = random.randint(lower, upper)
    main_alg(r)
write_in_file(circles, args.output_file)

# $ python social_distancing.py -i 11 --min_radius 2 --max_radius 25 -s 9 hello.txt
