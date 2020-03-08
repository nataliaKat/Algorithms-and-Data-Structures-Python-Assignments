import sys
from pprint import pprint

def find_adj(x, y, n):
    neighbours = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    for nei in neighbours[:]:
        if not ((nei[1] > 0 or nei[1] == 0 and nei[0] >= 0) and (abs(nei[0]) + nei[1] < n)):
            neighbours.remove(nei) 
    return neighbours


def make_graph():
    n = int(sys.argv[2]) if sys.argv[1] == "-p" else int(sys.argv[1])

    g = {}
    for i in range (-n + 2, n):
        for j in range(n):
            if (j > 0 or j == 0 and i >= 0) and (abs(i) + j < n):
                g[(i, j)] = find_adj(i, j, n)

    if sys.argv[1] == "-p":
        pprint(g)


make_graph()

