from pysat.formula import CNF
from pysat.solvers import Glucose3
from array import *

# number of neurons
C = 1

# max weight
max = 5

# size of dataset
n = 3
m = 3


# gate input
k = n - 1


# literal counter
count = 1

# dataset dicts
w_str = {}
w_digit = {}

# output dicts
o_str = {}
o_digit = {}

# weight dicts
omega_str = {}
omega_digit = {}

# gate input dicts
i_str = {}
i_digit = {}


# simulation variable dicts
y_str = {}
y_digit = {}


def generate_dataset(m, n):
    global w_str
    global w_digit
    global count

    for i in range(m):
        for j in range(n):
            s = "w" + str(i+1) + str(j)
            w_str[s] = count
            w_digit[count] = s

            count += 1


def generate_outputs(c, m):
    global o_str
    global o_digit
    global count

    for a in range(c):
        for i in range(m):
            s = "o" + str(a+1) + str(i+1)
            o_str[s] = count
            o_digit[count] = s

            count += 1


def generate_weights(c, max):
    global omega_str
    global omega_digit
    global count

    for a in range(c):
        for v in range(max):
            s = "omega" + str(a+1) + str(v)
            omega_str[s] = count
            omega_digit[count] = s

            count += 1


def generate_gate_inputs(c, m, k):
    global i_str
    global i_digit
    global count

    for a in range(c):
        for i in range(m):
            for b in range(k):
                s = "i" + str(a+1) + str(i+1) + str(b+1)
                i_str[s] = count
                i_digit[count] = s

                count += 1


def generate_simulation_variables(c, m, k, max):
    global y_str
    global y_digit
    global count

    for a in range(c):
        for i in range(m):
            for b in range(k):
                for v in range(max):
                    s = "y" + str(a+1) + str(i+1) + str(b+1) + str(v)
                    y_str[s] = count
                    y_digit[count] = s
                    count += 1


generate_dataset(m, n)
generate_outputs(C, m)
generate_weights(C, max)
generate_gate_inputs(C, m, k)
generate_simulation_variables(C, m, k, max)


formula = CNF()

# print("w:", w_str)
# print("i:", i_str)

# create clauses relating dataset variables with gate input variables (should be equivalent)


def relate_w_i(c, m, k):

    for a in range(c):
        for i in range(m):
            for b in range(k):
                w_key = "w" + str(i + 1) + str(b+1)
                i_key = "i" + str(a+1) + str(i + 1) + str(b+1)
                formula.append([i_str[i_key], -w_str[w_key]])
                formula.append([-i_str[i_key], w_str[w_key]])

# relate_w_i(C, m, k)
# print(formula.clauses)


# print("w:", w_str)
# print("o:", o_str)


# create clauses relating dataset labels with output variables (they should be equivalent)
def relate_w_o(c, m):
    for a in range(c):
        for i in range(m):
            w_key = "w" + str(i + 1) + str(0)
            o_key = "o" + str(a+1) + str(i + 1)
            formula.append([w_str[w_key], -o_str[o_key]])
            formula.append([-w_str[w_key], o_str[o_key]])


# relate_w_o(C, m)

# print(formula.clauses)

# print("y", y_str)
# print()
# print("omega", omega_str)
# print()
# print("o", o_str)
# print()


# create clauses relating output variables with weight variables and simulations variables
def relate_y_omega_o(c, m, max):
    for a in range(c):
        for i in range(m):
            for v in range(max):
                for v_prime in range(max):
                    if v_prime >= v:
                        y_key = "y" + str(a + 1) + str(i + 1) + \
                            str(k) + str(v_prime)
                        o_key = "o" + str(a+1) + str(i + 1)
                        omega_key = "omega" + str(a + 1) + str(v)
                        formula.append(
                            [-y_str[y_key], -omega_str[omega_key], o_str[o_key]])


# relate_y_omega_o(C, m, max)
# print(formula.clauses)
# print("Y:", y_str)
# print()


def uniqueness_y(c, m, k, max):
    for a in range(c):
        for i in range(m):
            for b in range(k):
                for v in range(max):
                    for v_prime in range(max):
                        if v != v_prime:
                            y_key_1 = "y" + str(a + 1) + \
                                str(i + 1) + str(b+1) + str(v)
                            y_key_2 = "y" + \
                                str(a + 1) + str(i + 1) + \
                                str(b+1) + str(v_prime)
                            formula.append([y_str[y_key_1], -y_str[y_key_2]])


# uniqueness_y(C, m, k, max)

# print(formula.clauses)

print("Omega:", omega_str)


def uniqueness_omega(c, max):
    for a in range(c):
        for v in range(max):
            for v_prime in range(max):
                if v != v_prime:
                    omega_key_1 = "omega" + str(a + 1) + str(v)
                    omega_key_2 = "omega" + str(a + 1) + str(v_prime)
                    formula.append([omega_str[omega_key_1], -omega_str[omega_key_2]])

uniqueness_omega(C, max)

print(formula.clauses)

# #dataset
# w = [
#     [1, 2, 3],
#     [-4, -5, -6],
#     [-7, 8, -9]
# ]

# # outputs (length is n of strings in dataset)
# o = [
#     [10, -11, -12]
# ]

# # gate weigth / threshold
# omega = [
#     [-13, -14, 15, -16, -17, -18, -19, -20, -21, -22]
# ]

# # gate input
# input = [
#     [

#         [23, 24],
#         [-25, -26],
#         [27, -28]
#     ]
# ]

# # simulation variables
# y = [
#     [
#         [-29, 30, -31, -32, -33, -34, -35, -36, -37, -38],
#         [-39, -40, 41, -42, -43, -44, -45, -46, -47, -48]
#     ],
#     [
#         [39, -40, -41, -42, -43, -44, -45, -46, -47, -48],
#         [49, -50, -51, -52, -53, -54, -55, -56, -57, -58]
#     ],
#     [
#         [-59, 60, -61, -62, -63, -64, -65, -66, -67, -68],
#         [-69, 70, -71, -72, -73, -74, -75, -76, -77, -78]
#     ],
# ]

# def get_data_entry(i):

#     return w[i]

# def get_output(i):
#     return o[i]

# def get_input_bit(gate, i, b):
#     return input[gate][i][b]

# def get_threshold(gate):
#     for i in omega:
#         if (omega[i] > 0):
#             return i


# def formula(dataset):

#     k = 2

#     solver = Glucose3()
#     for i in range(len(dataset)):
#         print("data:")
#         print(i)
#         for b in range(1, k):
#                 print("i:")
#                 print(i)
#                 print("B:")
#                 print(b-1)
#                 solver.add_clause([input[0][i][b-1], dataset[i][b-1] * -1])
#                 solver.add_clause([input[0][i][b-1] * -1, dataset[i][b-1]]),
#                 solver.add_clause([w[i][0], o[0][i] * -1]),
#                 solver.add_clause([w[i][0]*-1, o[0][i]]),
#                 for v in range(len(omega[0])):
#                     # add all clauses for when v' >= v. also add all clauses for when v != v' for the others
#                     if (omega[0][v] > 0):
#                         for v_, var in enumerate(y[i][k-1], start=v):
#                             print("i:")
#                             print(i)
#                             print("k:")
#                             print(k-1)
#                             print("v_:")
#                             print(v_)
#                             print(y[i][k-1][v_])
#                             #solver.add_clause(y[i][k-1][v_] * -1, omega[0][v])

#         print("end")

# formula(w)


# # create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
# cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

# # create a SAT solver for this formula:
# with Solver(bootstrap_with=cnf) as solver:
#     # 1.1 call the solver for this formula:
#     print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

#     # 1.2 the formula is satisfiable and so has a model:
#     print('and the model is:', solver.get_model())

#     # 2.1 apply the MiniSat-like assumption interface:
#     print('formula is',
#         f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
#         'assuming x1 and x2')

#     # 2.2 the formula is unsatisfiable,
#     # i.e. an unsatisfiable core can be extracted:
#     print('and the unsatisfiable core is:', solver.get_core())
