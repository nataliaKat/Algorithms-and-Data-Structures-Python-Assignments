import argparse
from pprint import pprint

def find_adj(x, y, g):
    """ Finds the neighbours of a node
        
        Parameters
        ----------
        x : int
            x-coordinate of node
        y : int
            y-coordinate of node
        g : dictionary
            the graph

        Returns
        -------
        list
            the neighbours of the node, at most 4
    """

    neighbours = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    for nei in neighbours[:]:
        # Checks if it exists in the graph
        if not nei in g.keys():
            neighbours.remove(nei) 
    return neighbours

def make_graph(n):
    """
        Constructs a graph containing the polyominoes

        Parameters
        ----------
        n : int
            size of polyomino
        
        Returns
        -------
        g : dictionary
            a graph containing the polyominoes

    """
    g = {}
    for i in range (-n + 2, n):
        for j in range(n):
            if (j > 0 or j == 0 and i >= 0) and (abs(i) + j < n):
                g[(i, j)] = []   
    for k in g.keys():
        g[k] = find_adj(k[0], k[1], g)
    return g

def count_fixed_polyominoes(g, untried, n, p, counter):
    """ Recursively counts the different polyominoes made with n nodes.

        Parameters
        ----------
        g : dictionary
            a graph containing the polyominoes
        untried : set
            a set of nodes
        n : int
            the size of polyominos
        p : list
            the current polyomino
        counter : Counter
            a counter

        Returns
        -------
        int
            number of fixed polyominoes        
    """

    while untried:
        u = untried.pop()
        p.append(u)
        if len(p) == n:
            counter.c += 1
        else:
            new_neighbors = set()
            u_neighbors = g.get(u)
            other_neighbors = [k for a in p if a != u for k in g[a]]
            for v in u_neighbors:
                if v not in untried and v not in p and v not in other_neighbors:
                    new_neighbors.add(v)
            new_untried = untried | new_neighbors
            count_fixed_polyominoes(g, new_untried, n, p, counter)
        p.remove(u)
    return counter.c

class Counter:
    c = 0

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--print", help="print graph", action="store_true")
parser.add_argument("n", type=int, help="size of polyomino")

args = parser.parse_args()
g = make_graph(args.n)
if args.print:
    pprint(g)
counter = Counter()

print(count_fixed_polyominoes(g, {(0,0)}, args.n, [], counter))
