import math


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
    return round(math.sqrt(c[0] ** 2 + c[1] ** 2) - c[2], 2)


def get_circle_nearest_to_beginning(circles):
    return min(circles, key=lambda k: k[1])


def do_circles_intersect(c1, c2):
    dist = round(math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2), 2)
    if dist < c1[2] + c2[2]:
        return True
    return False


def get_intersecting_circle(battlefront, ci, cm):
    circles = set()
    for c in battlefront:
        if do_circles_intersect(ci, c):
            circles.add(c)
    if len(circles) != 0:
        return min(circles, key=lambda k: math.sqrt((cm[0] - k[0]) ** 2 + (cm[1] - k[1]) ** 2))
    return 0


def delete_from_battlefront_dict(battlefront, key):
    previous = get_previous(battlefront, key)
    next = get_next(battlefront, key)
    del battlefront[key]
    update_next(battlefront, previous, next)
    update_previous(battlefront, next, previous)
    return battlefront


def step5(battlefront, ci, cm, cn, cj, battlefront_in_order):
    semicircle = len(battlefront) // 2
    in_semicircle = False
    current = cm
    for i in range(semicircle):
        current = get_previous(battlefront, current)
        if current == ci:
            in_semicircle = True
            break
    if in_semicircle:
        a = get_next(battlefront, cj)
        while a != cn:
            print(a)
            x = get_next(battlefront, a)
            battlefront = delete_from_battlefront_dict(battlefront, a)
            # battlefront_in_order.remove(a)
            a = x
        return 1
    else:
        a = get_previous(battlefront, cj)
        while a != cn:
            x = get_previous(battlefront, a)
            battlefront = delete_from_battlefront_dict(battlefront, a)
            # battlefront_in_order.remove(a)
            a = x
    return 2

def write_in_file(circles, filename):
    f = open(filename, 'w')
    for c in circles:
        line = str(c[0]) + ' ' + str(c[1]) + ' ' + str(c[2]) + '\n'
        f.write(line)
    f.close()


r = 2
c1 = (0, 0, r)
c2 = (0, 2 * r, r)
battlefront = {c1: [c2, c2],
               c2: [c1, c1]
               }
battlefront_in_order = [(c1, find_circle_distance_from_00(
    c1)), (c2, find_circle_distance_from_00(c2))]
circles = [c1, c2]
print(battlefront)
cm = get_circle_nearest_to_beginning(battlefront_in_order)[0]
for i in range(150):
    cn = get_next(battlefront, cm)
    ci = find_tangent_circle(cm, cn, r)
    inters = get_intersecting_circle(battlefront, ci, cm)
    if inters == 0:
        battlefront[ci] = [cm, cn]
        update_previous(battlefront, cn, ci)
        update_next(battlefront, cm, ci)
        battlefront_in_order.append((ci, find_circle_distance_from_00(ci)))
        circles.append(ci)
    else:
        if step5(battlefront, ci, cm, cn, inters, battlefront_in_order) == 1:
            cm = inters
        else:
            cn = inters

    # for c in battlefront:
    #     if get_next(battlefront, c) == cm:
    #         ci = c

write_in_file(circles, "output_file")
