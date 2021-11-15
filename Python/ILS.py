import copy
import os
import random
import re
import sys
import time

# filepath_rm = os.path.join(
#     'C:\\Users\\Bruno\\Desktop\\UFRGS\\Semestre5\\otimizacao\\final-otimizacao\\instances', 'RM12')
# filepath_ans = os.path.join('/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao/Julia','answer_12.txt')
# filepath_rm = os.path.join('/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao/rm','RM01')
filepath_rm = '/home/leo/Documents/2021_1/Otimizacao/Trabalho/final-otimizacao/rm'


chars = "x[](),\n"


class State:
    def __init__(self, sol, remaining_edges, vertices, types, value=None):
        self.sol = sol
        self.remaining_edges = remaining_edges
        self.vertices = vertices
        self.types = types
        self.value = len(sol)

    def generate_neighbor(self):

        size = len(self.remaining_edges)

        while(size > 0):
            r = random.randint(0, size-1)

            if test_edge(self, self.remaining_edges[r]):

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


def open_rm(file):
    filepath = os.path.join(filepath_rm, file)

    edges = []
    with open(filepath) as f:
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


def generate_initial_state(file, max_rand):
    filepath = os.path.join(filepath_rm, file)
    sol = []
    rm = open_rm(filepath)
    chosen_vertices = []
    chosen_types = []

    r = random.randint(0, int(max_rand))
    for _ in range(r):
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


def local_search(current_state):
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


def test_edge(current_state, candidate_edge):

    if candidate_edge[0] in current_state.vertices or candidate_edge[1] in current_state.vertices:
        return False

    if candidate_edge[2] in current_state.types:
        return False

    return True


def shake(current_state, level, rm):

    new_state = State(current_state.sol, [], current_state.vertices,
                      current_state.types, current_state.value)

    for i in range(level):
        r = random.randint(0, new_state.value-1)
        removed_edge = new_state.sol.pop(r)
        new_state.vertices.remove(removed_edge[0])
        new_state.vertices.remove(removed_edge[1])
        new_state.types.remove(removed_edge[2])
        new_state.value -= 1

    for i in range(len(rm)):
        if(test_edge(new_state, rm[i])):
            new_state.remaining_edges.append(rm[i])

    return new_state


def ils(rm, file, arguments):
    initial_state = generate_initial_state(file, arguments[0])
    state = local_search(initial_state)
    best_state = copy.deepcopy(state)
    iterations = 5000
    level = 1
    step = int(arguments[1])
    
    timeout = time.time() + 60*2

    while(iterations != 0):
        iterations -= 1
        start_pert = time.time()
        state = shake(best_state, level, rm)
        print(f'iteration {iterations}')
        print(time.time() - start_pert, " segundos")
        state = local_search(state)
        print(len(state.sol))
        if len(state.sol) >= 2440:
            print(len(rm))
            print(test_answer(state.sol))
        if state.value > best_state.value:
            best_state = state
            level = 1
        else:
            level += step
            if level > best_state.value-1:
                level = best_state.value-1
        if time.time() > timeout:
            break
    return best_state


def test_answer(ans):
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


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(f'Número incorreto de argumentos. Esperava 5 e recebeu {len(sys.argv)}')
        exit(1)
    random.seed(int(sys.argv[2]))
    arguments = sys.argv[3:]

    filepath = input('Digite o nome do arquivo: ')

    rm = open_rm(filepath)
    s = ils(rm, filepath, arguments)

    print('Melhor solução encontrada: \n')
    print(s.sol)
    print(s.value)

    with open(sys.argv[1], "w") as f:
        f.write(str(s.value) + '\n')
        for i in s.sol:
            f.write(str(i) + '\n')

    # with open("answers_ils.txt", "a") as f:
    #     f.write('*'*12)
    #     f.write(sys.argv[1] + '\n')
    #     f.write(str(s.value) + '\n')
    #     f.write(str(test_answer(s.sol)) + '\n')
