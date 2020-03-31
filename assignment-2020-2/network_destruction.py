from pprint import pprint
import argparse
from collections import deque

def create_graph_from_file(input_filenane):
    g = {}
    with open(input_filenane) as graph_input:
        for line in graph_input:
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            g[nodes[0]].append(nodes[1])
            g[nodes[1]].append(nodes[0])
    return g

def get_number_of_neighbours(g, node):
    return len(g[node])

def get_max_edges_node(g):
    return max(g, key=lambda k: get_number_of_neighbours(k))

def remove_node(g, node):
    for x in g:
        if node in g[x]:
            g[x].remove(node)
    del g[node]
    return g

def destroy1(g, n):
    for i in range(n):
        max_edges_node = get_max_edges_node(g)
        print(max_edges_node, get_number_of_neighbours(max_edges_node))
        remove_node(g, max_edges_node)

def get_uball(g, i, r):
    ball = set()
    q = deque()
    max_node = max(g)
    visited = [False for k in range(max_node)]
    inqueue = [False for k in range(max_node)]
    visited.append(False)
    inqueue.append(False)

    level = 0
    q.appendleft((i, level))
    inqueue[i] = True

    while not len(q) == 0 and level <= r:
        c = q.pop()
        c_node = c[0]
        level = c[1]
        inqueue[c_node] = False
        visited[c_node] = True
        if level == r:
            ball.add(c_node)
        for v in g[c_node]:
            if not visited[v] and not inqueue[v]:
                q.appendleft((v, level + 1))
                inqueue[v] = True

    return ball
                                    
def get_collective_influence(g, r):
    u_balls = {k: get_uball(g, k, r) for k in g.keys()}
    ci = {}
    for k in u_balls:
        sum = 0
        for i in u_balls[k]:
            sum += get_number_of_neighbours(g, i) - 1
        ci[k] = (get_number_of_neighbours(g, k) - 1)* sum
    return ci
    # temp_neighbours = {k: get_number_of_neighbours(g, k) - 1 for k in g.keys()}
    # return {k: (get_number_of_neighbours(g, k) - 1) * sum(temp_neighbours[i]) for k in g.keys() for i in u_balls[k]}

def destroy2(g, n, r):
    for i in range(n):
        ci = get_collective_influence(g, r)
        max_ci = max(g, key=lambda k: ci[k])
        print(max_ci, ci[max_ci])
        remove_node(g, max_ci)
        # ci = get_collective_influence(g, r + 1)
        # pprint(ci)

    
    # max(g, key=lambda k: g[k])

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="use simple algorithm", action="store_true")
parser.add_argument("-r", type=int, help="radius")
parser.add_argument("num_nodes", type=int, help="number of nodes to be removed")
parser.add_argument("input_file", help="name of file")

args = parser.parse_args()
if args.c:
    destroy1(create_graph_from_file(args.input_file), args.num_nodes)
else:
    # get_collective_influence(create_graph_from_file(args.input_file), args.r)
    destroy2(create_graph_from_file(args.input_file), args.num_nodes, args.r)
