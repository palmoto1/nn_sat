from nn_sat import *
from data_set_generator import *
from evaluation import *
import csv

import time

generator = DatasetGenerator()
evaluator = Evaluation()

#Ensure that the model fits the dataset correctly by increasing the length of n with the power 2,
# i.e. n = 8 → n = 16 → n = 32 etc. d, l and dataset_size are constant.
# def experiment1(depth, layer_size, dataset_size):
#     print('EXPERIMENT 1')
#     n = 8
#     while(i < 500):
        
#         print('i:', i)
#         generator.create_model(depth, layer_size, n)
#         generator.create_inputs(dataset_size, n, "./generated_dataset.csv")
#         print('Dataset generated')  # TEST - EXPERIMENT
        
#         run_nn_sat("./generated_dataset.csv")
        
#         evaluator.create_model("./model.csv")
#         evaluator.evaluate_dataset("./generated_dataset.csv")
        
#         i *= 2
        
# #Investigates the relation between d and time for computing the network. l, n and dataset_size are constant.
# def experiment2(n, layer_size, dataset_size):
#     print('EXPERIMENT 2')

#     d = 1
#     running = True
    
#     while(running):
#         print('d:', d)
#         generator.create_model(d, layer_size, n)
#         generator.create_inputs(dataset_size, n, "./generated_dataset.csv")
#         print('Dataset generated')  # TEST - EXPERIMENT
        
#         start = time.time()
#         run_nn_sat("./generated_dataset.csv")
#         stop = time.time()
        
#         evaluator.create_model("./model.csv")
#         evaluator.evaluate_dataset("./generated_dataset.csv")
        
#         execution_time = stop - start
#         print('Execution time (sec): ', execution_time)
        
#         if(execution_time/60 >= 10):
#             running = False
        
#         d += 1
#         print()


#Investigates the influence of d with the number of activated neurons at layer d.
#I.e. If d = 10, how many neurons are activated in that layer?
def experiment3(n, layer_size, dataset_size, no_of_datasets):
    print('EXPERIMENT 3')

    result = []
    d = no_of_datasets

    generator.create_dataset(d, layer_size, dataset_size, n, 0.8, "./experiments/experiment3/datasets/dataset1.csv")

    inputs = []

    with open("./experiments/experiment3/datasets/dataset1.csv", "r") as file:
            csvreader = csv.reader(file)
            for input in csvreader:
                if input[0] != 'header' and input[0] != 'end':
                    inputs.append(input)

    for i in range(1, no_of_datasets + 1):
        header = ["header", d, layer_size]
        with open("./experiments/experiment3/datasets/dataset" + str(i) +".csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(inputs)
            writer.writerow(["end"])

        run_nn_sat("./experiments/experiment3/datasets/dataset" + str(i) + ".csv", "./experiments/experiment3/models/model" + str(i) + ".csv")

        evaluator.create_model("./experiments/experiment3/models/model" + str(i) + ".csv")
        evaluator.evaluate_dataset("./experiments/experiment3/datasets/dataset" + str(i) + ".csv")

        result.append(["Dataset_" + str(i)])
        for key in range(1, len(evaluator.total_activated_neurons)):
             result.append(["Depth: " + str(key) + " Activated neurons: " + str(evaluator.total_activated_neurons[key])])
        result.append(["end"])

        d += no_of_datasets
    
    with open("./experiments/experiment3/result/activated_neurons.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerows(result)

    


#Given a neural network with d layers, try to synthesize a network with d - 1 layers and see 
#if it still correctly fits the model. Same goes for l.
# def experiment4(n, depth, layer_size, dataset_size):
#     print('EXPERIMENT 4')
    
#     print('d:', d, '\nl: ', layer_size)
#     generator.create_model(depth, layer_size, n)
#     generator.create_inputs(dataset_size, n, "./generated_dataset.csv")
#     print('Dataset generated')  # TEST - EXPERIMENT
    
#     run_nn_sat("./generated_dataset.csv")

#     evaluator.create_model("./model.csv")
#     evaluator.evaluate_dataset("./generated_dataset.csv")


        
#experiment1(2, 4, 100)
#experiment2(10, 8, 100)
experiment3(10, 5, 2, 5)
