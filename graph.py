import numpy as np
import random
colors = {0: 'NONE', 1: 'RED', 2: 'GREEN', 3: 'BLUE', 4: 'WHITE', 5: 'BLACK', 6: 'YELLOW', 7: 'CYAN'}


class Vertex:
    ass_time = 0
    def __init__(self, index):
        self.index = index
        self.color = 0
        self.ass_time = -1
        self.possible_values = colors
        self.neighbours = []

    def __str__(self):
        return "({},{})".format(self.index, colors[self.color])

    def is_assigned(self):
        return self.color

    def assign(self, val):
        assert val in self.possible_values
        self.color = val
        self.ass_time = Vertex.ass_time
        Vertex.ass_time += 1
        self.possible_values


class Edge:
    def __init__(self, a, b):
        self.vertex_a = a
        self.vertex_b = b

    def __str__(self):
        return "({},{})".format(self.vertex_a, self.vertex_b)


def parse_graphfile(graph_filename):
    """
    These graphs are in a modification of the DIMACS file format. Each line of the graph begins with a letter that defines the rest of the line. The legal lines are

    c Comment: remainder of line ignored.

    p Problem: must be of form
        p edges n m
        where n is the number of nodes (to be numbered 1..n) and m the number of edges.

    e Edge: must be of the form
        e n1 n2 d
        where n1 and n2 are the endpoints of the edge. The optional d value is used to enforce a requirement and n1 and n2 have colors that differ by at least d (if there is no d value, it is assumed d=1).

    f Fixed: of the form
        f n1 c1 c2 c3 ...
        states that node n1 must choose its colors from c1, c2, c3 ... (the default is that the node can take on any color).

    n Node: of the form
        n n1 c1
        used in multicoloring to state that c1 colors must be assigned to node n1. Any node without a "n" line is assumed to have value 1. These colors must all differ by at least 1, unless there is an edge of the form

        e n1 n1 d
        in which case all the colors at n1 must differ by at least d.
    """
    comments = ""
    edges = []
    vertices = []

    with open(graph_filename, 'r') as graph_file:
        for line in graph_file:
            # print(line)
            ll = line.split(' ')

            prefix = ll[0]
            if prefix == 'c':
                comments = comments + line[2:] + '\n'
            elif prefix == 'p':
                num_edges = ll[2]
                num_vertices = ll[3].split('\n')[0]
                print('Edges: {}'.format(num_edges))
                print('Vertices: {}'.format(num_vertices))
                for idx in range(int(num_vertices)):
                    vertices.append(Vertex(idx + 1))
            elif prefix == 'e':
                idx_a = int(ll[1])
                idx_b = int(ll[2].split('\n')[0])
                edges.append(Edge(vertices[idx_a - 1], vertices[idx_b - 1]))
                vertices[idx_a - 1].neighbours.append(vertices[idx_b - 1])
                vertices[idx_b - 1].neighbours.append(vertices[idx_a - 1])
            elif prefix == 'f':
                print('f: Not supported yet')
            elif prefix == 'n':
                print('n: Not supported yet')

    return comments, edges, vertices


class Graph:
    def __init__(self):
        self.comments = ""
        self.edges = []
        self.vertices = []

    def __str__(self):
        edges_to_print = ""
        vertices_to_print = ""
        for e in self.edges:
            edges_to_print = edges_to_print + str(e)
        for v in self.vertices:
            vertices_to_print = vertices_to_print + str(v)

        output = "Edges: " + edges_to_print + "\n" + \
                 "Vertices: " + vertices_to_print + "\n"
        return output

    def read_graph(self, filename):
        self.comments, self.edges, self.vertices = parse_graphfile(filename)

    def pick_unassigned_var(self, hueristic=None):
        indexes = np.array(range(len(self.vertices)))
        # random.shuffle(indexes)
        for idx in indexes:
            if not self.vertices[idx].is_assigned():
                return self.vertices[idx]
        return None

    def all_var_assigned(self):
        var = self.pick_unassigned_var()
        if var is None:
            return True
        else:
            return False

    def get_possible_values(self, var):
        used_colors = np.zeros(len(colors)-1)
        for varn in var.neighbours:
            varn_col = varn.color
            if varn_col != 0:
                used_colors[varn_col - 1] = 1
                if sum(used_colors) == len(colors)-1:
                    return []
        return [i + 1 for i, c in enumerate(used_colors) if c == 0]

    def get_erliest_in_conflict_set(self, var):
        conflict_set =  [n for n in var.neighbours if n.color != 0]
        chronology = [n.ass_time for n in var.neighbours if n.color != 0]
        earliest_idx = chronology.index(min(chronology))
        return conflict_set[earliest_idx]

    def get_possible_values2(self, var):
        used_colors = np.zeros(len(colors)-1)
        for e in self.edges:
            var_col = 0
            if var.index == e.vertex_a:
                var_col = self.vertices[e.vertex_b - 1].color
            elif var.index == e.vertex_b:
                var_col = self.vertices[e.vertex_a - 1].color
            if var_col != 0:
                used_colors[var_col - 1] = 1
                if sum(used_colors) == len(colors)-1:
                    return []
        return [i + 1 for i, c in enumerate(used_colors) if c == 0]
