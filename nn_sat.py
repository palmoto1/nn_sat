from pysat.formula import CNF
from pysat.solvers import Glucose3
from array import *

# number of neurons
C = 1

# max weight
max = 3

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

# create clauses relating dataset variables with gate input variables (should be equivalent)
def relate_w_i(c, m, k):

    for a in range(c):
        for i in range(m):
            for b in range(k):
                w_key = "w" + str(i + 1) + str(b+1)
                i_key = "i" + str(a+1) + str(i + 1) + str(b+1)
                formula.append([i_str[i_key], -w_str[w_key]])
                formula.append([-i_str[i_key], w_str[w_key]])

relate_w_i(C, m, k)

# create clauses relating dataset labels with output variables (they should be equivalent)
def relate_w_o(c, m):
    for a in range(c):
        for i in range(m):
            w_key = "w" + str(i + 1) + str(0)
            o_key = "o" + str(a+1) + str(i + 1)
            formula.append([w_str[w_key], -o_str[o_key]])
            formula.append([-w_str[w_key], o_str[o_key]])


relate_w_o(C, m)

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


relate_y_omega_o(C, m, max)

# def uniqueness_y(c, m, k, max):
#     for a in range(c):
#         for i in range(m):
#             for b in range(k):
#                 for v in range(max):
#                     for v_prime in range(max):
#                         if v != v_prime:
#                             y_key_1 = "y" + str(a + 1) + \
#                                 str(i + 1) + str(b+1) + str(v)
#                             y_key_2 = "y" + \
#                                 str(a + 1) + str(i + 1) + \
#                                 str(b+1) + str(v_prime)
#                             formula2.append([y_str[y_key_1], -y_str[y_key_2]])

def uniqueness_y_2(c, m, k, max):
    for a in range(c):
        for i in range(m):
            for b in range(k):
                clause = []
                for v in range(max):
                    y_key_1 = "y" + str(a + 1) + \
                                str(i + 1) + str(b+1) + str(v)
                    clause.append(y_str[y_key_1])
                    for v_prime in range(v+1,max):            
                        y_key_2 = "y" + \
                            str(a + 1) + str(i + 1) + \
                            str(b+1) + str(v_prime)
                        formula.append([-y_str[y_key_1], -y_str[y_key_2]])

                formula.append(clause)


uniqueness_y_2(C, m, k, max)

# def uniqueness_omega(c, max):
#     for a in range(c):
#         for v in range(max):
#             for v_prime in range(max):
#                 if v != v_prime:
#                     omega_key_1 = "omega" + str(a + 1) + str(v)
#                     omega_key_2 = "omega" + str(a + 1) + str(v_prime)
#                     formula.append(
#                         [omega_str[omega_key_1], -omega_str[omega_key_2]])
                    

def uniqueness_omega_2(c, max):
    for a in range(c):
        clause = []
        for v in range(max):
            omega_key_1 = "omega" + str(a + 1) + str(v)
            clause.append(omega_str[omega_key_1])
            for v_prime in range(v+1, max):
                omega_key_2 = "omega" + str(a + 1) + str(v_prime)
                formula.append(
                    [-omega_str[omega_key_1], -omega_str[omega_key_2]])
        formula.append(clause)


uniqueness_omega_2(C, max)

# relates input bit 1 of string i so that it is logically equivalent to the simulation variable with weight 1
def relate_partial_sums_inputs_0(c, m):
    for a in range(c):
        for i in range(m):
            i_key = "i" + str(a+1) + str(i + 1) + str(1)
            y_key = "y" + str(a + 1) + \
                            str(i + 1) + str(1) + str(1)
            formula.append([i_str[i_key], -y_str[y_key]])
            formula.append([-i_str[i_key], y_str[y_key]])
            
relate_partial_sums_inputs_0(C, max)


def relate_partial_sums_inputs_1(c, m, k, max):
    for a in range(c):
        for i in range(m):
            for b in range(k):
                for v in range(max):
                    if b != k-1 and v != max-1:
                        y_key_1 = "y" + str(a + 1) + \
                            str(i + 1) + str(b+1) + str(v)
                        y_key_2 = "y" + \
                            str(a + 1) + str(i + 1) + \
                            str(b+2) + str(v +1)
                        i_key = "i" + str(a+1) + str(i + 1) + str(b+2)
                        formula.append([-y_str[y_key_1], -i_str[i_key], y_str[y_key_2]])

relate_partial_sums_inputs_1(C, m, k, max)

def relate_partial_sums_inputs_2(c, m, k, max):
    for a in range(c):
        for i in range(m):
            for b in range(k):
                for v in range(max):
                    if b != k-1:
                        y_key_1 = "y" + str(a + 1) + \
                            str(i + 1) + str(b+1) + str(v)
                        y_key_2 = "y" + \
                            str(a + 1) + str(i + 1) + \
                            str(b+2) + str(v)
                        i_key = "i" + str(a+1) + str(i + 1) + str(b+2)
                        formula.append([-y_str[y_key_1], i_str[i_key], y_str[y_key_2]])

relate_partial_sums_inputs_2(C, m, k, max)


dataset = [
    [1, 1, 1],
    [0, 0, 0],
    [0, 1, 0]
]

assumptions = []

def fit_data():
    for i in range(m):
        for j in range(n):
            s = "w" + str(i+1) + str(j)
            if dataset[i][j] < 1:
                assumptions.append(w_str[s] * -1)
            else:
                assumptions.append(w_str[s])
                
def merge_dicts(*dicts):
    result = {}
    for dict in dicts:
        result = result | dict
        
    return result
                
def translate_model(model):
    dict = merge_dicts(w_digit, o_digit, i_digit, omega_digit, y_digit)
    translation = []
    for i in model:
        if i < 0:
            s = '-' + dict[i * -1]
            translation.append(s)
        else:
            translation.append(dict[i])
        
    return translation
        


fit_data() 

g = Glucose3()

g.append_formula(formula)

print(formula.clauses)
print()

solution = g.solve(assumptions=assumptions)

print(w_str)
print()
print(i_str)
print()
print(o_str)
print()
print(omega_str)
print()
print(y_str)
print()


print(solution)
model = g.get_model()
print(model)
print(translate_model(model))



