from pprint import pprint
import argparse
from collections import deque
from graphviz import Graph

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

def draw_graph(g, name_param):
    gr = Graph(format="png", name="graph" + name_param)
    edges = []
    for k in g.keys():
        gr.node(str(k), color="red")
        for n in g[k]:
            if n < k:
                gr.edge(str(k), str(n), color="red") 
    gr.view()

def get_number_of_neighbours(g, node):
    return len(g[node])

def get_max_edges_node(g):
    return max(g, key=lambda k: get_number_of_neighbours(g, k))

def remove_node(g, node):
    for x in g:
        if node in g[x]:
            g[x].remove(node)
    del g[node]
    return g

def destroy1(g, n, draw=False):
    for i in range(n):
        max_edges_node = get_max_edges_node(g)
        print(max_edges_node, get_number_of_neighbours(g, max_edges_node))
        remove_node(g, max_edges_node)
        if draw:
            draw_graph(g, str(i))

def get_ball(g, i, r):
    ball = set()
    uball = set()
    q = deque()
    max_node = max(g)
    visited = [False for k in range(max_node + 1)]
    inqueue = [False for k in range(max_node + 1)]

    level = 0
    q.appendleft((i, level))
    inqueue[i] = True

    while not len(q) == 0 and level <= r:
        c = q.pop()
        c_node = c[0]
        level = c[1]
        inqueue[c_node] = False
        visited[c_node] = True
        if level != 0:
            ball.add(c_node)
        if level == r:
            uball.add(c_node)
        for v in g[c_node]:
            if not visited[v] and not inqueue[v]:
                q.appendleft((v, level + 1))
                inqueue[v] = True
    # position 0: in and at the surface of the ball
    # position 1: only at the surface
    return (ball, uball)

def get_collective_influence(g, node, r):
    u_balls = get_ball(g, node, r)[1]
    sum = 0
    for i in u_balls:
        sum += get_number_of_neighbours(g, i) - 1
    ci = (get_number_of_neighbours(g, node) - 1) * sum
    return ci

def destroy2(g, n, r, draw=False):
    ci = {k: get_collective_influence(g, k, r) for k in g.keys()}
    for i in range(n):
        # pprint(ci)
        max_ci = max(g, key=lambda k: ci[k])
        print(max_ci, ci[max_ci])
        ball_of_removed = get_ball(g, max_ci, r + 1)[0]
        remove_node(g, max_ci)
        if draw:
            draw_graph(g, str(i))
        for k in ball_of_removed:
            ci[k] = get_collective_influence(g, k, r)

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="use simple algorithm", action="store_true")
parser.add_argument("-t", help="trace graph", action="store_true")
parser.add_argument("-r", type=int, help="radius")
parser.add_argument("num_nodes", type=int, help="number of nodes to be removed")
parser.add_argument("input_file", help="name of file")

args = parser.parse_args()
if args.c:
    destroy1(create_graph_from_file(args.input_file), args.num_nodes, args.t)
else:
    destroy2(create_graph_from_file(args.input_file), args.num_nodes, args.r, args.t)
