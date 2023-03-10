from pysat.formula import CNF
from pysat.solvers import Glucose3
from array import *
import csv

# better naming of variables

formula = CNF()
solver = Glucose3()
file_path = "./test.csv"

dataset = []
assumptions = []

# number of neurons (not needed?)
C = 0

# depth of netork
d = 0

# layer size
l = 0

# maximum weight
max = 0

# size of dataset
n = 0
m = 0

# gate input
k = 0

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


def generate_dataset_variables(m, n):
    global w_str
    global w_digit
    global count

    for i in range(m):
        for j in range(n):
            s = "w" + str(i+1) + str(j)
            w_str[s] = count
            w_digit[count] = s

            count += 1


def generate_outputs(m, depth, layer_size):
    global o_str
    global o_digit
    global count
    for i in range(m):
        for d in range(depth):
            for l in range(layer_size):
                s = "o" + str(i+1) + str(d+1) + str(l+1)
                o_str[s] = count
                o_digit[count] = s
                count += 1
        
        # last gate (final output)
        s = "o" + str(i+1) + str(depth + 1) + str(1)
        o_str[s] = count
        o_digit[count] = s
        count += 1


def generate_weights(depth, layer_size, max):
    global omega_str
    global omega_digit
    global count

    for d in range(depth):
        for l in range(layer_size):
            for v in range(max):
                s = "omega" + str(d+1) + str(l+1) + str(v)
                omega_str[s] = count
                omega_digit[count] = s
                count += 1
    
    # last gate (final output)
    for v in range(max):
        s = "omega" + str(depth+1) + str(1) + str(v)
        omega_str[s] = count
        omega_digit[count] = s
        count += 1


def generate_gate_inputs(depth, layer_size, m, k):
    global i_str
    global i_digit
    global count


    for i in range(m):
        for d in range(depth):
            for l in range(layer_size):
                gate_inputs = range(k) if d == 0 else range(layer_size) # every gate in first layer should have k dataset bits as inputs 
                for b in gate_inputs:
                    s = "i" + str(i+1) + str(d+1) + str(l+1) + str(b+1)
                    i_str[s] = count
                    i_digit[count] = s
                    count += 1
        for b in range(layer_size):
            s = "i" + str(i+1) + str(depth+1) + str(1) + str(b+1)            
            i_str[s] = count
            i_digit[count] = s
            count += 1
    



# def generate_simulation_variables(c, m, k, max):
#     global y_str
#     global y_digit
#     global count

#     for a in range(c):
#         for i in range(m):
#             for b in range(k):
#                 for v in range(max):
#                     s = "y" + str(a+1) + str(i+1) + str(b+1) + str(v)
#                     y_str[s] = count
#                     y_digit[count] = s
#                     count += 1

# generate all variables
def generate_variables():
    generate_dataset_variables(m, n)
    generate_outputs(m, d, l)
    generate_weights(d, l, max)
    generate_gate_inputs(d, l, m, k)
    # generate_simulation_variables(C, m, k, max)


# create clauses relating dataset variables with gate input variables (should be equivalent)
# def relate_w_i(c, m, k):

#     for a in range(c):
#         for i in range(m):
#             for b in range(k):
#                 w_key = "w" + str(i + 1) + str(b+1)
#                 i_key = "i" + str(a+1) + str(i + 1) + str(b+1)
#                 formula.append([i_str[i_key], -w_str[w_key]])
#                 formula.append([-i_str[i_key], w_str[w_key]])


# # create clauses relating dataset labels with output variables (they should be equivalent)
# def relate_w_o(c, m):
#     for a in range(c):
#         for i in range(m):
#             w_key = "w" + str(i + 1) + str(0)
#             o_key = "o" + str(a+1) + str(i + 1)
#             formula.append([w_str[w_key], -o_str[o_key]])
#             formula.append([-w_str[w_key], o_str[o_key]])


# # create clauses relating output variables with weight variables and simulations variables
# def relate_y_omega_o(c, m, max):
#     for a in range(c):
#         for i in range(m):
#             for v in range(max):
#                 for v_prime in range(max):
#                     if v_prime >= v:
#                         y_key = "y" + str(a + 1) + str(i + 1) + \
#                             str(k) + str(v_prime)
#                         o_key = "o" + str(a+1) + str(i + 1)
#                         omega_key = "omega" + str(a + 1) + str(v)
#                         formula.append(
#                             [-y_str[y_key], -omega_str[omega_key], o_str[o_key]])


# # def uniqueness_y(c, m, k, max):
# #     for a in range(c):
# #         for i in range(m):
# #             for b in range(k):
# #                 for v in range(max):
# #                     for v_prime in range(max):
# #                         if v != v_prime:
# #                             y_key_1 = "y" + str(a + 1) + \
# #                                 str(i + 1) + str(b+1) + str(v)
# #                             y_key_2 = "y" + \
# #                                 str(a + 1) + str(i + 1) + \
# #                                 str(b+1) + str(v_prime)
# #                             formula2.append([y_str[y_key_1], -y_str[y_key_2]])

# # define the uniqueness of simulation variables, i.e. of n variables there can only be one that is true while the rest have to be false
# def uniqueness_y(c, m, k, max):
#     for a in range(c):
#         for i in range(m):
#             for b in range(k):
#                 clause = []
#                 for v in range(max):
#                     y_key_1 = "y" + str(a + 1) + \
#                         str(i + 1) + str(b+1) + str(v)
#                     clause.append(y_str[y_key_1])
#                     for v_prime in range(v+1, max):
#                         y_key_2 = "y" + \
#                             str(a + 1) + str(i + 1) + \
#                             str(b+1) + str(v_prime)
#                         formula.append([-y_str[y_key_1], -y_str[y_key_2]])

#                 formula.append(clause)



# # def uniqueness_omega(c, max):
# #     for a in range(c):
# #         for v in range(max):
# #             for v_prime in range(max):
# #                 if v != v_prime:
# #                     omega_key_1 = "omega" + str(a + 1) + str(v)
# #                     omega_key_2 = "omega" + str(a + 1) + str(v_prime)
# #                     formula.append(
# #                         [omega_str[omega_key_1], -omega_str[omega_key_2]])

# # define the uniqueness of gate weight variables, just like for the simulation variables
# def uniqueness_omega(c, max):
#     for a in range(c):
#         clause = []
#         for v in range(max):
#             omega_key_1 = "omega" + str(a + 1) + str(v)
#             clause.append(omega_str[omega_key_1])
#             for v_prime in range(v+1, max):
#                 omega_key_2 = "omega" + str(a + 1) + str(v_prime)
#                 formula.append(
#                     [-omega_str[omega_key_1], -omega_str[omega_key_2]])
#         formula.append(clause)


# # creates clauses that relates input bit 1 of string i so that it is logically equivalent to the simulation variable with weight 1
# def relate_partial_sums_inputs_0(c, m):
#     for a in range(c):
#         for i in range(m):
#             i_key = "i" + str(a+1) + str(i + 1) + str(1)
#             y_key_0 = "y" + str(a + 1) + \
#                 str(i + 1) + str(1) + str(0)
#             y_key_1 = "y" + str(a + 1) + \
#                 str(i + 1) + str(1) + str(1)
#             formula.append([-i_str[i_key], -y_str[y_key_0]])
#             formula.append([i_str[i_key], y_str[y_key_0]])
#             formula.append([i_str[i_key], -y_str[y_key_1]])
#             formula.append([-i_str[i_key], y_str[y_key_1]])


# # creates clauses that relates the partial sums with the inputs
# def relate_partial_sums_inputs_1(c, m, k, max):
#     for a in range(c):
#         for i in range(m):
#             for b in range(k):
#                 for v in range(max):
#                     if b != k-1 and v != max-1:
#                         y_key_1 = "y" + str(a + 1) + \
#                             str(i + 1) + str(b+1) + str(v)
#                         y_key_2 = "y" + \
#                             str(a + 1) + str(i + 1) + \
#                             str(b+2) + str(v + 1)
#                         i_key = "i" + str(a+1) + str(i + 1) + str(b+2)
#                         formula.append(
#                             [-y_str[y_key_1], -i_str[i_key], y_str[y_key_2]])


# # creates clauses that relates the partial sums with the inputs
# def relate_partial_sums_inputs_2(c, m, k, max):
#     for a in range(c):
#         for i in range(m):
#             for b in range(k):
#                 for v in range(max):
#                     if b != k-1:
#                         y_key_1 = "y" + str(a + 1) + \
#                             str(i + 1) + str(b+1) + str(v)
#                         y_key_2 = "y" + \
#                             str(a + 1) + str(i + 1) + \
#                             str(b+2) + str(v)
#                         i_key = "i" + str(a+1) + str(i + 1) + str(b+2)
#                         formula.append(
#                             [-y_str[y_key_1], i_str[i_key], y_str[y_key_2]])


# def generate_formula():
#     relate_w_i(C, m, k)
#     relate_w_o(C, m)
#     relate_y_omega_o(C, m, max)
#     uniqueness_y(C, m, k, max)
#     uniqueness_omega(C, max)
#     relate_partial_sums_inputs_0(C, m)
#     relate_partial_sums_inputs_1(C, m, k, max)
#     relate_partial_sums_inputs_2(C, m, k, max)


# # create assumptions for the dataset variables
# def fit_data():
#     for i in range(m):
#         for j in range(n):
#             s = "w" + str(i+1) + str(j)
#             if dataset[i][j] < 1:
#                 assumptions.append(w_str[s] * -1)
#             else:
#                 assumptions.append(w_str[s])


# def merge_dicts(*dicts):
#     result = {}
#     for dict in dicts:
#         result = result | dict

#     return result


# def translate_model(model):
#     dict = merge_dicts(w_digit, o_digit, i_digit, omega_digit, y_digit)
#     translation = []
#     for i in model:
#         if i < 0:
#             s = '-' + dict[i * -1]
#             translation.append(s)
#         else:
#             translation.append(dict[i])

#     return translation

# def get_accepted_weight(translated_model):
#     for entry in translated_model:
#         if entry.startswith("omega"):
#             return entry
        
#     return "not found"


def reset():
    global solver
    global formula
    global dataset
    global assumptions

    global C
    global max
    global n
    global m
    global k
    global count
    
    global w_str
    global w_digit
    global o_str
    global o_digit
    global omega_str
    global omega_digit
    global i_str
    global i_digit
    global y_str
    global y_digit  
    
    formula = CNF()

    solver.delete()
    solver = Glucose3()

    dataset = []
    assumptions = []

    C = 0
    max = 0
    n = 0
    m = 0
    k = 0
    count = 1

    w_str = {}
    w_digit = {}

    o_str = {}
    o_digit = {}

    omega_str = {}
    omega_digit = {}

    i_str = {}
    i_digit = {}

    y_str = {}
    y_digit = {}

def main():
    global solver
    global formula
    global dataset
    global assumptions
    global solution

    global C
    global d
    global l
    global max
    global n
    global m
    global k

    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row[0] == 'end':
                m = len(dataset)
                n = len(dataset[0])
                k = n -1

                generate_variables()
                # print(w_str)
                # print(o_str)
                # print(omega_str)
                print(i_str)
                # generate_formula()

                # fit_data()

                # solver.append_formula(formula)
                # solution = solver.solve(assumptions)
                # model = solver.get_model()
                # print(model)
                # translated_model = translate_model(model)

                # print("Model: ", translated_model)
                # print("Weight: ", get_accepted_weight(translated_model))

                reset()
            elif row[0] == 'header':
                d = int(row[1])
                l = int(row[2])
                C = int(row[1]) * int(row[2]) + 1
                max = int(row[3])
            else:
                a = []
                for s in row:
                    a.append(int(s))   
                dataset.append(a)
                

# execute script
main()


# print(w_str)
# print()
# print(i_str)
# print()
# print(o_str)
# print()
# print(omega_str)
# print()
# print(y_str)
# print()


# print(solution)
# print(model)
# print()
# print(translated_model)
# print(get_accepted_weight(translated_model))
