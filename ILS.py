import os
import re
import random
import copy
import time

filepath_rm = os.path.join(
    'C:\\Users\\Bruno\\Desktop\\UFRGS\\Semestre5\\otimizacao\\final-otimizacao\\instances', 'RM12')
# filepath_ans = os.path.join('/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao/Julia','answer_12.txt')
# filepath_rm = os.path.join('/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao/rm','jcole.txt')


chars = "x[](),\n"


class State:
    def __init__(self, sol, remaining_edges, vertices, types, value=None):
        self.sol = sol
        self.remaining_edges = remaining_edges
        self.vertices = vertices
        self.types = types
        self.value = len(sol)

    def __str__(self):
        pass

    def generate_neighbor(self):

        size = len(self.remaining_edges)

        while(size > 0):
            r = random.randint(0, size-1)

            if teste(self, self.remaining_edges[r]):

                self.sol.append(self.remaining_edges[r])
                self.vertices.append(self.remaining_edges[r][0])
                self.vertices.append(self.remaining_edges[r][1])
                self.types.append(self.remaining_edges[r][2])
                self.remaining_edges.pop(r)
                self.value += 1
                return self

            self.remaining_edges.pop(r)
            size -= 1
        return self


def open_rm():
    edges = []
    with open(filepath_rm) as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()

        for line in f:
            l = line
            l = re.sub('[x[](),]', '', l)
            l = re.sub('\n', '', l)
            l = " ".join(l.split()).split(' ')
            l2 = []
            for a in l:
                l2.append(int(a))
            edges.append(l2)

    return edges


def generate_initial_state():
    random.seed(10)
    sol = []
    rm = open_rm()
    chosen_vertices = []
    chosen_types = []

    # print(len(rm))

    r = random.randint(0, 2500)
    for i in range(r):
        r2 = random.randint(0, len(rm))
        rand_edge = rm[r2]
        if rand_edge[0] not in chosen_vertices:
            if rand_edge[1] not in chosen_vertices:
                if rand_edge[2] not in chosen_types:
                    chosen_vertices.append(rand_edge[0])
                    chosen_vertices.append(rand_edge[1])
                    chosen_types.append(rand_edge[2])
                    sol.append(rand_edge)
                    rm.pop(r2)

    return State(sol, rm, chosen_vertices, chosen_types, len(sol))


def busca_local(current_state, rm):
    #print('busca local')
    new_state = current_state.generate_neighbor()
    better = True
    best_value = new_state.value

    while(better):
        better = False
        new_state = new_state.generate_neighbor()
        if new_state.value > best_value:
            best_value = new_state.value
            better = True
    return new_state


def teste(current_state, candidate_edge):

    if candidate_edge[0] in current_state.vertices or candidate_edge[1] in current_state.vertices:
        return False

    if candidate_edge[2] in current_state.types:
        return False

    return True


def perturbation(current_state, level, rm):

    new_state = State(current_state.sol, [], current_state.vertices,
                      current_state.types, current_state.value)

    print(f'perturbation: {level}')
    for i in range(level):
        r = random.randint(0, new_state.value-1)
        removed_edge = new_state.sol.pop(r)
        new_state.vertices.remove(removed_edge[0])
        new_state.vertices.remove(removed_edge[1])
        new_state.types.remove(removed_edge[2])
        new_state.value -= 1

    for i in range(len(rm)):
        if(teste(new_state, rm[i])):
            new_state.remaining_edges.append(rm[i])

    return new_state


def ils(rm):
    initial_state = generate_initial_state()
    state = busca_local(initial_state, rm)
    print(state.value)
    best_state = copy.deepcopy(state)
    iterations = 5000
    level = 1
    while(iterations != 0):
        start = time.time()
        iterations -= 1
        state = perturbation(state, level, rm)
        print(time.time() - start, " segundos")
        state = busca_local(state, rm)
        print(state.value)

        if state.value > best_state.value:
            best_state = state
            level = 1
        else:
            level += 1

    return best_state


def test_answer(rm, ans):
    edges = []
    ks = []

    for i in range(len(ans)):
        edges.append(ans[i][0])
        edges.append(ans[i][1])
        ks.append(ans[i][2])

    if len(edges) != len(set(edges)):
        return False

    if len(ks) != len(set(ks)):
        return False

    return True


rm = open_rm()
s = ils(rm)

print(s.sol)
print(s.value)
print(test_answer(rm, s.sol))


# for a in range(1000):
#   print(rm[a])
