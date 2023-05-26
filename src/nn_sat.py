from pysat.formula import CNF
from pysat.solvers import Glucose3
from array import *
import csv


formula = CNF()
solver = Glucose3()

dataset = []
assumptions = []

# depth of netork
d = 0

# layer size
l = 0

# maximum weight
max = 0

# size of dataset
n = 0
m = 0

# no of bits in a string
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
            s = "w" + '_' + str(i+1) + '_' + str(j)
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
                s = "o" + '_' + str(i+1) + '_' + str(d+1) + '_' + str(l+1)
                o_str[s] = count
                o_digit[count] = s
                count += 1
        
        # last gate (final output)
        s = "o" + '_' + str(i+1) + '_' + str(depth + 1) + '_' + str(1)
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
                s = "omega" + '_' + str(d+1) + '_' + str(l+1) + '_' + str(v)
                omega_str[s] = count
                omega_digit[count] = s
                count += 1
    
    # last gate (final output)
    for v in range(max):
        s = "omega" + '_' + str(depth+1) + '_' + str(1) + '_' + str(v)
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
                    s = "i" + '_' + str(i+1) + '_' + str(d+1) + '_' + str(l+1) + '_' + str(b+1)
                    i_str[s] = count
                    i_digit[count] = s
                    count += 1
        # last gate (final output)
        for b in range(layer_size):
            s = "i" + '_' + str(i+1) + '_' + str(depth+1) + '_' + str(1) + '_' + str(b+1)            
            i_str[s] = count
            i_digit[count] = s
            count += 1
    

def generate_simulation_variables(depth, layer_size, m, k, max):
    global y_str
    global y_digit
    global count

    for i in range(m):
        for d in range(depth):
            for l in range(layer_size):
                gate_inputs = range(k) if d == 0 else range(layer_size) # every gate in first layer should have k dataset bits as inputs 
                for b in gate_inputs:
                    for v in range(max):
                        s = "y" + '_' + str(i+1) + '_' + str(d+1) + '_' + str(l+1) + '_' + str(b+1) + '_' + str(v)
                        y_str[s] = count
                        y_digit[count] = s
                        count += 1
        # last gate (final output)
        for b in range(layer_size):
            for v in range(max):
                        s = "y" + '_' + str(i+1) + '_' + str(depth+1) + '_' + str(1) + '_' + str(b+1) + '_' + str(v)
                        y_str[s] = count
                        y_digit[count] = s
                        count += 1


# generate all variables
def generate_variables():
    generate_dataset_variables(m, n)
    generate_outputs(m, d, l)
    generate_weights(d, l, max)
    generate_gate_inputs(d, l, m, k)
    generate_simulation_variables(d, l, m, k, max)


# create clauses relating dataset variables with gate input variables of the first layer (should be equivalent)
def relate_w_i(layer_size, m, k):

    for i in range(m):
        for l in range(layer_size):
            for b in range(k):
                w_key = "w" + '_' + str(i + 1) + '_' + str(b+1)
                i_key = "i" + '_' + str(i+1) + '_' + str(1) +  '_' + str(l+1) + '_' + str(b+1)
                formula.append([i_str[i_key], -w_str[w_key]])
                formula.append([-i_str[i_key], w_str[w_key]])


# create clauses relating gate output variables with gate input variables of the following layer (should be equivalent)
def relate_o_i(depth, layer_size, m):

    for i in range(m):
        for d in range(depth + 1):
            if (d != 0):
                for l in range(layer_size):
                    for b in range(layer_size):
                        i_key = "i" + '_' + str(i+1) + '_' + str(d+1) + '_' + str(l+1) + '_' + str(b+1)
                        o_key = "o" + '_' + str(i + 1) + '_' + str(d) + '_' + str(b+1)
                        formula.append([i_str[i_key], -o_str[o_key]])
                        formula.append([-i_str[i_key], o_str[o_key]])
                    if d == depth:
                        break
        

# # create clauses relating dataset labels with output variables of the last gate in the network (they should be equivalent)
def relate_w_o(depth, m):
    
    for i in range(m):
        w_key = "w" + '_' + str(i + 1) + '_' + str(0)
        o_key = "o" + '_' + str(i+1) + '_' + str(depth+1) + '_' + str(1)
        formula.append([w_str[w_key], -o_str[o_key]])
        formula.append([-w_str[w_key], o_str[o_key]])


# create clauses relating output variables with weight variables and simulations variables
def relate_y_omega_o(depth, layer_size, m, max, poitive_output):

    if poitive_output:
        condition = lambda v_prime, v: v_prime >= v
    else:
        condition = lambda v_prime, v: v_prime < v 
    
    for i in range(m):
        for d in range(depth+1):
            b = k if d == 0 else layer_size # since the first layer has string bits as inputs
            for l in range(layer_size):
                for v in range(max):
                    for v_prime in range(max):
                        if condition(v_prime, v):
                            y_key = "y" + '_' + str(i+1) + '_' + str(d+1) + '_' + str(l+1) + '_' + str(b) + '_' + str(v_prime)
                            omega_key = "omega" + '_' + str(d + 1) + '_' + str(l+1) + '_' + str(v)
                            o_key = "o" + '_' + str(i+1) + '_' + str(d + 1) + '_' + str(l+1)
                            formula.append(
                                [-y_str[y_key], -omega_str[omega_key], o_str[o_key] if poitive_output else -o_str[o_key]])
                                
                                
                            
                if d == depth: # if we are at the output layer we only want to add clauses for the single output gate so we break here
                    break


# define the uniqueness of simulation variables, i.e. of n variables there can only be one that is true while the rest have to be false
def uniqueness_y(depth, layer_size, m, k, max):
    for i in range(m):
        for d in range(depth + 1):
            a = k if d == 0 else layer_size # since the first layer has string bits as inputs
            for l in range(layer_size):    
                t = 1 if d == depth else l + 1 # last layer only has one gate (output layer)
                for b in range(a):
                    clause = []
                    for v in range(max):
                        y_key_1 = "y" + '_' + str(i + 1) + \
                            '_' + str(d + 1) + '_' + str(t) + '_' + str(b+1) + '_' + str(v)
                        clause.append(y_str[y_key_1])
                        for v_prime in range(v+1, max):
                            y_key_2 = "y" + '_' + str(i + 1) + \
                            '_' + str(d + 1) + '_' + str(t) + '_' + str(b+1) + '_' + str(v_prime)
                            formula.append([-y_str[y_key_1], -y_str[y_key_2]])

                    formula.append(clause)
                if d == depth: # if we are at the output layer we only want to add clauses for the single output gate so we break here
                    break


# define the uniqueness of gate weight variables, just like for the simulation variables
def uniqueness_omega(depth, layer_size, max):
    for d in range(depth + 1):
        for l in range(layer_size):    
            t = 1 if d == depth else l + 1 # last layer only has one gate (output layer)
            clause = []
            for v in range(max):
                omega_key_1 = "omega" + '_' + str(d + 1) + '_' + str(t) + '_' + str(v)
                clause.append(omega_str[omega_key_1])
                for v_prime in range(v+1, max):
                    omega_key_2 = "omega" + '_' + str(d + 1) + '_' + str(t) + '_' + str(v_prime)
                    formula.append(
                    [-omega_str[omega_key_1], -omega_str[omega_key_2]])

            formula.append(clause)
            if d == depth: # if we are at the output layer we only want to add clauses for the single output gate so we break here
                break


# creates clauses that relates input bit 1 of string i so that it is logically equivalent to the simulation variable with weight 1 or 0 depending on its value
def relate_i_y(depth, layer_size, m):
        for i in range(m):
            for d in range(depth + 1):
                for l in range(layer_size):
                    i_key = "i" + '_' + str(i+1) + '_' + str(d + 1) + '_' + str(l+1) + '_' + str(1)
                    y_key_0 = "y" + '_' + str(i + 1) + \
                        '_' + str(d + 1) + '_' + str(l+1) + '_' + str(1) + '_' + str(0)
                    y_key_1 = "y" + '_' + str(i + 1) + \
                        '_' + str(d + 1) + '_' + str(l+1) + '_' + str(1) + '_' + str(1)
                    formula.append([-i_str[i_key], -y_str[y_key_0]])
                    formula.append([i_str[i_key], y_str[y_key_0]])
                    formula.append([i_str[i_key], -y_str[y_key_1]])
                    formula.append([-i_str[i_key], y_str[y_key_1]])

                    if d == depth:
                        break


# creates clauses that relates the partial sums with the inputs
def relate_partial_sums_inputs(depth, layer_size, m, k, max, positive_input):
        
        if positive_input:
            condition = lambda b, gate_inputs, v, max: b != gate_inputs-1 and v != max-1
            j = 1
        else:
            condition = lambda b, gate_inputs, v, max: b != gate_inputs-1
            j = 0

        for i in range(m):
            for d in range(depth + 1):
                for l in range(layer_size):
                    gate_inputs = k if d == 0 else layer_size # every gate in first layer should have k dataset bits as inputs 
                    for b in range(gate_inputs):
                        for v in range(max):
                            if condition(b, gate_inputs, v, max):
                                y_key_1 = "y" + '_' + str(i + 1) + \
                                    '_' + str(d + 1) + '_' + str(l+1) + '_' + str(b+1) + '_' + str(v)
                                y_key_2 = "y" + '_' + str(i + 1) + \
                                    '_' + str(d + 1) + '_' + str(l+1) + '_' + str(b+2) + '_' + str(v+j)
                                i_key = "i" + '_' + str(i+1) + '_' + str(d + 1) + '_' + str(l+1) + '_' + str(b+2)
                                formula.append(
                                    [-y_str[y_key_1], -i_str[i_key] if positive_input else i_str[i_key], y_str[y_key_2]])
                    if d == depth:
                        break


def generate_formula():
    relate_w_i(l, m, k)
    relate_o_i(d, l, m)
    relate_w_o(d, m)
    relate_y_omega_o(d, l, m, max, True)
    relate_y_omega_o(d, l, m, max, False)
    uniqueness_y(d, l, m, k, max)
    uniqueness_omega(d, l, max)
    relate_i_y(d, l, m)
    relate_partial_sums_inputs(d, l, m, k, max, True)
    relate_partial_sums_inputs(d, l, m, k, max, False)


# # create assumptions for the dataset variables
def fit_data():
    for i in range(m):
        for j in range(n):
            s = "w" + '_' + str(i+1) + '_' + str(j)
            if dataset[i][j] < 1:
                assumptions.append(w_str[s] * -1)
            else:
                assumptions.append(w_str[s])


def merge_dicts(*dicts):
    result = {}
    for dict in dicts:
        result = result | dict

    return result


# translates model to strings instead of digits
def translate_model(model):
    if not model:
        return None
    dict = merge_dicts(w_digit, o_digit, i_digit, omega_digit, y_digit)
    translation = []
    for i in model:
        if i < 0:
            s = '-' + dict[i * -1]
            translation.append(s)
        else:
            translation.append(dict[i])

    return translation


# gets only the weight variables
def get_accepted_weights(translated_model):
    if not translate_model:
        return ["no_solution"]
    result = []
    for entry in translated_model:
        if entry.startswith("omega"):
            result.append([entry])
        
    return result


def get_positive_outputs(translated_model):
    result = []
    for entry in translated_model:
        if entry[0] == 'o' and entry[1] != 'm':
            result.append(entry)
        
    return result


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


# main function
def run_nn_sat(dataset_path, model_path):
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

    with open(dataset_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row[0] == 'end':
                m = len(dataset)
                n = len(dataset[0])
                k = n -1

                max = l + 1 if l >= n else n
                #print('max: ', max) #TEST
                generate_variables()
                print('Variables generated')  # TEST - EXPERIMENT
                generate_formula()
                print('Forumla generated')  # TEST - EXPERIMENT

                fit_data()

                solver.append_formula(formula)
                solution = solver.solve(assumptions)
                print('Solution found: ', solution) 
                model = solver.get_model()

                translated_model = translate_model(model)

                accepted_weights = get_accepted_weights(translated_model)
                #positive_outputs = get_positive_outputs(translated_model)

                #print("Model: ", translated_model)
                #print("Weights: ", accepted_weights) 
                #print("Outputs: ", positive_outputs)

                # write gate thresholds to file used in evaluation
                with open(model_path, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerows(accepted_weights)

                reset()
            elif row[0] == 'header':
                d = int(row[1])
                l = int(row[2])
            else:
                a = []
                for s in row:
                    a.append(int(s))   
                dataset.append(a)
                
# THIS CALL CAN BE USED FOR TESTING

#run_nn_sat("./generated_dataset.csv", "./model.csv")

