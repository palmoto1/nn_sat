from nn_sat import *
from src.data_set_generator import *
from src.evaluation import *
import csv

import time

generator = DatasetGenerator()
evaluator = Evaluation()

# Ensure that the model fits the dataset correctly by increasing the length of n with the power 2,
# i.e. n = 8 → n = 16 → n = 32 etc. d, l and dataset_size are constant.
def experiment1(start, factor, range, depth, layer_size, dataset_size):
    print('EXPERIMENT 1')
    result = []
    n = start
    i = 1
    while(n < range):
        
        print('n:', n)
        generator.create_dataset(depth, layer_size, dataset_size, n, 0.8, "./experiments/experiment1/datasets/dataset" + str(i) + ".csv")

        print('Dataset generated')
        
        run_nn_sat("./experiments/experiment1/datasets/dataset" + str(i) + ".csv", "./experiments/experiment1/models/model" + str(i) + ".csv")
        
        evaluator.create_model("./experiments/experiment1/models/model" + str(i) + ".csv")
        evaluation = evaluator.evaluate_dataset("./experiments/experiment1/datasets/dataset" + str(i) + ".csv")

        result.append(["Dataset_" + str(i)])
        result.append(["Input string length: " + str(n) + " Evaluation: " + str(evaluation)])
        result.append(["end"])
        
        n *= factor
        i += 1

    with open("./experiments/experiment1/result/evaluations.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerows(result)
        
# #Investigates the relation between d and time for computing the network. l, n and dataset_size are constant.
def experiment2(n, layer_size, dataset_size, time_limit_minutes):
    print('EXPERIMENT 2')
    result = []

    d = 1
    running = True
    
    while(running):
        print('d:', d)
        generator.create_dataset(d, layer_size, dataset_size, n, 0.8, "./experiments/experiment2/datasets/dataset" + str(d) + ".csv")

        print('Dataset generated')  # TEST - EXPERIMENT
        
        start = time.time()
        run_nn_sat("./experiments/experiment2/datasets/dataset" + str(d) + ".csv", "./experiments/experiment2/models/model" + str(d) + ".csv")
        stop = time.time()
        
        evaluator.create_model("./experiments/experiment2/models/model" + str(d) + ".csv")
        evaluation = evaluator.evaluate_dataset("./experiments/experiment2/datasets/dataset" + str(d) + ".csv")
        
        execution_time = stop - start
        #print('Execution time (sec): ', execution_time)

        result.append(["Dataset_" + str(d)])
        result.append(["Depth: " + str(d) + " Evaluation: " + str(evaluation) + " Execution time (seconds): " + str(execution_time)])
        result.append(["end"])
        
        if(execution_time/60 >= time_limit_minutes):
            running = False
        
        d += 1

    with open("./experiments/experiment2/result/execution_times.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerows(result)


#Investigates the influence of d with the number of activated neurons at layer d.
#I.e. If d = 10, how many neurons are activated in that layer?
def experiment3(n, depth_step, layer_size, dataset_size, no_of_datasets, dataset_groups):
    print('EXPERIMENT 3')

    
    for i in range(1, no_of_datasets + 1):
        generator.create_dataset(depth_step, layer_size, dataset_size, n, 0.8, "./experiments/experiment3/datasets/dataset" + str(i) +".csv")
        inputs = []

        with open("./experiments/experiment3/datasets/dataset" + str(i) +".csv", "r") as file:
            csvreader = csv.reader(file)
            for input in csvreader:
                if input[0] != 'header' and input[0] != 'end':
                    inputs.append(input)

        d = depth_step * 2
        for j in range(1, dataset_groups):
            k = i + depth_step * j
            header = ["header", d , layer_size]
            with open("./experiments/experiment3/datasets/dataset" + str(k) +".csv", 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(inputs)
                writer.writerow(["end"])
            d += depth_step

    result = []
    for i in range(1, dataset_groups * no_of_datasets + 1):    
        #run_nn_sat("./experiments/experiment3/datasets/dataset" + str(i) + ".csv", "./experiments/experiment3/models/model" + str(i) + ".csv")

        evaluator.create_model("./experiments/experiment3/models/model" + str(i) + ".csv")
        evaluator.evaluate_dataset("./experiments/experiment3/datasets/dataset" + str(i) + ".csv")

        result.append(["Dataset_" + str(i)])
        for key in range(1, len(evaluator.total_activated_neurons)):
            result.append(["Depth: " + str(key) + " Activated neurons: " + str(evaluator.total_activated_neurons[key] / dataset_size)])
        result.append(["end"])

    
    with open("./experiments/experiment3/result/activated_neurons.csv", 'w') as file:
         writer = csv.writer(file)
         writer.writerows(result)

    
# Given a neural network with d layers, try to synthesize a network with d - 1 layers and see
# if it still correctly fits the model.
def experiment4_1(n, d, l, dataset_size):
    print('EXPERIMENT 4.1')

    result = []

    original_dataset_path = "./experiments/experiment4-1/datasets/dataset" + \
        str(d) + ".csv"

    generator.create_dataset(d, l, dataset_size, n,
                             0.8, original_dataset_path)

    inputs = []
    with open(original_dataset_path, "r") as file:
        csvreader = csv.reader(file)
        for input in csvreader:
            if input[0] != 'header' and input[0] != 'end':
                inputs.append(input)

    #Create and evaluate d-1 model from original dataset
    for i in reversed(range(1, d+1)):
        header = ["header", i, l]
        with open("./experiments/experiment4-1/datasets/dataset" + str(i) + ".csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(inputs)
            writer.writerow(["end"])

        run_nn_sat("./experiments/experiment4-1/datasets/dataset" + str(i) +
                   ".csv", "./experiments/experiment4-1/models/model" + str(i) + ".csv")

        evaluator.create_model(
            "./experiments/experiment4-1/models/model" + str(i) + ".csv")
        evaluation = evaluator.evaluate_dataset(
            "./experiments/experiment4-1/datasets/dataset" + str(i) + ".csv")

        result.append(["Dataset_" + str(i)])
        result.append(["Depth: " + str(i) + " Evaluation: " + str(evaluation)])
        result.append(["end"])

    with open("./experiments/experiment4-1/result/smaller_model_1.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerows(result)



# Given a neural network with l neurons/layer, try to synthesize a network with l - 1 neurons/layer and see
# if it still correctly fits the model.
def experiment4_2(n, d, l, dataset_size):
    print('EXPERIMENT 4.2')
    result = []

    original_dataset_path = "./experiments/experiment4-2/datasets/dataset" + \
        str(l) + ".csv"

    generator.create_dataset(d, l, dataset_size, n,
                             0.8, original_dataset_path)

    inputs = []
    with open(original_dataset_path, "r") as file:
        csvreader = csv.reader(file)
        for input in csvreader:
            if input[0] != 'header' and input[0] != 'end':
                inputs.append(input)

    #Create and evaluate l-1 model from original dataset
    for i in reversed(range(1, l+1)):
        header = ["header", d, i]
        with open("./experiments/experiment4-2/datasets/dataset" + str(i) + ".csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(inputs)
            writer.writerow(["end"])

        run_nn_sat("./experiments/experiment4-2/datasets/dataset" + str(i) +
                   ".csv", "./experiments/experiment4-2/models/model" + str(i) + ".csv")

        evaluator.create_model(
            "./experiments/experiment4-2/models/model" + str(i) + ".csv")
        evaluation = evaluator.evaluate_dataset(
            "./experiments/experiment4-2/datasets/dataset" + str(i) + ".csv")

        result.append(["Dataset_" + str(i)])
        result.append(["Layer size: " + str(i) + " Evaluation: " + str(evaluation)])
        result.append(["end"])

    with open("./experiments/experiment4-2/result/smaller_model_2.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerows(result)

# Given a neural network with depth d and l neurons/layer, try to synthesize a network with d -1 and l - 1 neurons/layer and see
# if it still correctly fits the model.
def experiment4_3(n, d, l, dataset_size):
    print('EXPERIMENT 4.3')
    result = []

    original_dataset_path = "./experiments/experiment4-3/datasets/dataset" + \
        str(l) + ".csv"

    generator.create_dataset(d, l, dataset_size, n,
                             0.8, original_dataset_path)

    inputs = []
    with open(original_dataset_path, "r") as file:
        csvreader = csv.reader(file)
        for input in csvreader:
            if input[0] != 'header' and input[0] != 'end':
                inputs.append(input)

    #Create and evaluate d-1 and l-1 model from original dataset
    i = min(d, l)
    current_d = d
    current_l = l
    while i > 0:
        header = ["header", current_d, current_l]
        with open("./experiments/experiment4-3/datasets/dataset" + str(i) + ".csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(inputs)
            writer.writerow(["end"])

        run_nn_sat("./experiments/experiment4-3/datasets/dataset" + str(i) +
                   ".csv", "./experiments/experiment4-3/models/model" + str(i) + ".csv")

        evaluator.create_model(
            "./experiments/experiment4-3/models/model" + str(i) + ".csv")
        evaluation = evaluator.evaluate_dataset(
            "./experiments/experiment4-3/datasets/dataset" + str(i) + ".csv")

        result.append(["Dataset_" + str(i)])
        result.append(["Depth: " + str(current_d) + " Layer size: " + str(current_l) + " Evaluation: " + str(evaluation)])
        result.append(["end"])

        i -= 1
        current_d -= 1
        current_l -= 1

    with open("./experiments/experiment4-3/result/smaller_model_3.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerows(result)


#experiment1(2, 2, 150, 10, 8, 10)
#experiment2(10, 8, 100)
#experiment2(n=25,layer_size=8, dataset_size=25, time_limit_minutes=10)
experiment3(n=10, depth_step=5, layer_size=8, dataset_size=10, no_of_datasets=5)
#experiment4_1(n=10, d=3, l=5, dataset_size=10)
#experiment4_2(n=10, d=3, l=5, dataset_size=10)
#experiment4_3(n=25, d=10, l=10, dataset_size=25)
