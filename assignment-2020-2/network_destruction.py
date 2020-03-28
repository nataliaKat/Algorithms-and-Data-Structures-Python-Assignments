from pprint import pprint


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


def get_max_edges_node(g):
    return max(g, key=lambda k: len(g[k]))


def remove_node(g, node):
    for x in g:
        if node in g[x]:
            g[x].remove(node)
    del g[node]


def destroy_1(g, n):
    for i in range(n):
        max_edges_node = get_max_edges_node(g)
        print(max_edges_node, len(g[max_edges_node]))
        remove_node(g, max_edges_node)


destroy_1(create_graph_from_file("destruction_example_1.txt"), 4)

# g = create_graph_from_file()
# get_max_edges_node()
