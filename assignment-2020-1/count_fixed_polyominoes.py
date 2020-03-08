import sys
from pprint import pprint

def find_adj(x, y, n):
    neighbours = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    for nei in neighbours[:]:
        if not ((nei[1] > 0 or nei[1] == 0 and nei[0] >= 0) and (abs(nei[0]) + nei[1] < n)):
            neighbours.remove(nei) 
    return neighbours

def make_graph(n):
    g = {}
    for i in range (-n + 2, n):
        for j in range(n):
            if (j > 0 or j == 0 and i >= 0) and (abs(i) + j < n):
                g[(i, j)] = find_adj(i, j, n)

    if sys.argv[1] == "-p":
        pprint(g)
    
    return g

def get_neighbors_but_from_u(g, u, p):
    nb = []
    for a in p:
        if a != u:
            for k in g[a]:
                nb.append(k)
    return nb

def count_fixed_polyominoes(g, untried, n, p, counter):
    while untried:
        u = untried.pop()
        p.append(u)
        if len(p) == n:
            counter.c += 1
        else:
            new_neighbors = set()
            u_neighbors = g.get(u)
            other_neighbors = get_neighbors_but_from_u(g, u, p)
            for v in u_neighbors:
                if v not in untried and v not in p and v not in other_neighbors:
                    new_neighbors.add(v)
            new_untried = untried | new_neighbors
            count_fixed_polyominoes(g, new_untried, n, p, counter)
        p.remove(u)
    return counter.c

class Counter:
    c = 0


n = int(sys.argv[2]) if sys.argv[1] == "-p" else int(sys.argv[1])
g = make_graph(n)
counter = Counter()

print(count_fixed_polyominoes(g, {(0,0)}, n, [], counter))


