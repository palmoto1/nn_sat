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

relate_w_i(C, m, k)
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


relate_w_o(C, m)

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


relate_y_omega_o(C, m, max)
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


uniqueness_y(C, m, k, max)

# print(formula.clauses)

print("Omega:", omega_str)


def uniqueness_omega(c, max):
    for a in range(c):
        for v in range(max):
            for v_prime in range(max):
                if v != v_prime:
                    omega_key_1 = "omega" + str(a + 1) + str(v)
                    omega_key_2 = "omega" + str(a + 1) + str(v_prime)
                    formula.append(
                        [omega_str[omega_key_1], -omega_str[omega_key_2]])


uniqueness_omega(C, max)

# # print(formula.clauses)

# print("Y: ", y_str)
# print()
# print("I: ", i_str)
# print()


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

# print(formula.clauses)


# print("Y: ", y_str)
# print()
# print("I: ", i_str)
# print()


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
                        formula.append([y_str[y_key_1], -i_str[i_key], y_str[y_key_2]])

relate_partial_sums_inputs_2(C, m, k, max)

# print(formula.clauses)

g = Glucose3()

g.append_formula(formula)

print(g.solve())

print(g.get_model())


