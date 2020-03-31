from collections import deque

g = {
    1: [5],
    2: [6],
    3: [6],
    4: [5],
    5: [1, 4, 6, 7, 8],
    6: [2, 3, 5, 9, 10],
    7: [5, 8],
    8: [5, 7, 9, 16],
    9: [6, 8, 10, 20],
    10: [6, 9, 11, 15],
    11: [10, 12, 17],
    12: [11, 13, 14, 18, 19],
    13: [12],
    14: [12, 19],
    15: [10, 25],
    16: [8, 17, 22, 24],
    17: [11, 16, 18, 26],
    18: [12, 17],
    19: [12, 14],
    20: [9, 25, 26],
    21: [22],
    22: [16, 21, 23, 24, 25],
    23: [22, 24],
    24: [16, 22, 23, 25, 27],
    25: [15, 20, 22, 24, 28, 29],
    26: [17, 20, 30],
    27: [24],
    28: [25, 29],
    29: [25, 28],
    30: [26]
}


def bfs(g, node):

    q = deque()

    visited = [False for k in g.keys()]
    inqueue = [False for k in g.keys()]
    visited.append(False)
    inqueue.append(False)
    q.appendleft(node)
    inqueue[node] = True

    while not (len(q) == 0):
        print("Queue", q)
        c = q.pop()
        print("Visiting", c)
        inqueue[c] = False
        visited[c] = True
        for v in g[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True

def get_uball(g, i, r):
    ball = set()
    q = deque()
    visited = [False for k in g.keys()]
    inqueue = [False for k in g.keys()]
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
                                    
# bfs(g, 1)

print(get_uball(g, 1, 3))
