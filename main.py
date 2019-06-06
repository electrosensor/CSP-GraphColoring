from graph import Graph as ColorGraph
from graph import colors
import numpy as np
import matplotlib.pyplot as plt

filename = 'DSJC125.1.col'
it = 0


def solve(g):
    global it
    var = g.pick_unassigned_var()
    values = g.get_possible_values(var)
    for val in values:
        var.assign(val)
        it += 1
        if g.all_var_assigned():
            return g
        print(g)
        return solve(g)
    return None


def solve_with_backjumping(g):
    global it
    print("Iteration: {}".format(it))
    var = g.pick_unassigned_var()
    values = g.get_possible_values(var)
    for val in values:
        var.assign(val)
        it += 1
        if g.all_var_assigned():
            return g
        print(g)
        return solve_with_backjumping(g)
    conflict_var = g.get_erliest_in_conflict_set(var)
    values = g.get_possible_values(conflict_var)
    values = [val for val in values if val != conflict_var.color]
    assert values
    var.assign(values[0])
    return solve_with_backjumping(g)


def csp():
    g = ColorGraph()
    g.read_graph(filename)
    print(g)
    solution = solve_with_backjumping(g)
    print("Solution: {}".format(solution))
    print("Iterations: {}".format(it))


if __name__ == '__main__':
    csp()
