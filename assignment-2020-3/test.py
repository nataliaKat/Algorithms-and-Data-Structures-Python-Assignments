g = {
    (0, 0) : [(0, 1), (1, 0)],
    (1, 0) : [(0, 0), (1, 1)],
    (1, 1) : [(1, 0), (8, 0)],
    (0, 1) : [(8, 0), (0, 0)],
    (8, 0) : [(1, 1), (0, 1)]
}

def get_previous(d, element):
    return list(d[element])[0]

def get_next(d, element):
    return list(d[element])[1]

def update_previous(battlefront, element, value):
    battlefront[element][0] = value


def update_next(battlefront, element, value):
    battlefront[element][1] = value

def delete_from_battlefront_dict(battlefront, key):
    previous = get_previous(battlefront, key)
    next = get_next(battlefront, key)
    del battlefront[key]
    update_next(battlefront, previous, next)
    update_previous(battlefront, next, previous)
    return battlefront


print(delete_from_battlefront_dict(g, (0, 0)))
print(delete_from_battlefront_dict(g, (1, 0)))
print(delete_from_battlefront_dict(g, (0, 1)))