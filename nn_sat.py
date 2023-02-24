from pysat.formula import CNF
from pysat.solvers import Glucose3
from array import *


#dataset
w = [
    [1, 2, 3],
    [-4, -5, -6],
    [-7, 8, -9]
]

# outputs (length is n of strings in dataset)
o = [
    [10, -11, -12]
]

# gate weigth / threshold
omega = [
    [-13, -14, 15, -16, -17, -18, -19, -20, -21, -22]
]

# gate input
input = [
    [
        
        [23, 24],
        [-25, -26],
        [27, -28]
    ]
]

# simulation variables
y = [
    [
        [-29, 30, -31, -32, -33, -34, -35, -36, -37, -38],
        [-39, -40, 41, -42, -43, -44, -45, -46, -47, -48]
    ],
    [
        [39, -40, -41, -42, -43, -44, -45, -46, -47, -48],
        [49, -50, -51, -52, -53, -54, -55, -56, -57, -58]
    ],
    [
        [-59, 60, -61, -62, -63, -64, -65, -66, -67, -68],
        [-69, 70, -71, -72, -73, -74, -75, -76, -77, -78]
    ],
]

def get_data_entry(i):

    return w[i]

def get_output(i):
    return o[i]

def get_input_bit(gate, i, b):
    return input[gate][i][b]

def get_threshold(gate):
    for i in omega:
        if (omega[i] > 0):
            return i






def formula(dataset):

    k = 2

    solver = Glucose3()
    for i in range(len(dataset)):
        print("data:")
        print(i)
        for b in range(1, k): 
                print("i:")
                print(i)
                print("B:")
                print(b-1)
                solver.add_clause([input[0][i][b-1], dataset[i][b-1] * -1]) 
                solver.add_clause([input[0][i][b-1] * -1, dataset[i][b-1]]),
                solver.add_clause([w[i][0], o[0][i] * -1]), 
                solver.add_clause([w[i][0]*-1, o[0][i]]),
                for v in range(len(omega[0])):
                    # add all clauses for when v' >= v. also add all clauses for when v != v' for the others
                    if (omega[0][v] > 0):
                        for v_, var in enumerate(y[i][k-1], start=v): 
                            print("i:")
                            print(i)
                            print("k:")
                            print(k-1)
                            print("v_:")
                            print(v_)
                            print(y[i][k-1][v_])
                            #solver.add_clause(y[i][k-1][v_] * -1, omega[0][v])

        print("end")

formula(w)


# create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

# create a SAT solver for this formula:
with Solver(bootstrap_with=cnf) as solver:
    # 1.1 call the solver for this formula:
    print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    # 1.2 the formula is satisfiable and so has a model:
    print('and the model is:', solver.get_model())

    # 2.1 apply the MiniSat-like assumption interface:
    print('formula is',
        f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
        'assuming x1 and x2')

    # 2.2 the formula is unsatisfiable,
    # i.e. an unsatisfiable core can be extracted:
    print('and the unsatisfiable core is:', solver.get_core())