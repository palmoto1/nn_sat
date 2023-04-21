from nn_sat import *
from data_set_generator import *
from evaluation import *

import time

generator = DatasetGenerator()
evaluator = Evaluation()

#Ensure that the model fits the dataset correctly by increasing the length of n with the power 2,
# i.e. n = 8 → n = 16 → n = 32 etc. d, l and dataset_size are constant.
def experiment1(depth, layer_size, dataset_size):
    print('EXPERIMENT 1')
    n = 8
    while(i < 500):
        
        print('i:', i)
        generator.create_model(depth, layer_size, n)
        generator.create_inputs(dataset_size, n, "./generated_dataset.csv")
        print('Dataset generated')  # TEST - EXPERIMENT
        
        run_nn_sat("./generated_dataset.csv")
        
        evaluator.create_model("./model.csv")
        evaluator.evaluate_dataset("./generated_dataset.csv")
        
        i *= 2
        
#Investigates the relation between d and time for computing the network. l, n and dataset_size are constant.
def experiment2(n, layer_size, dataset_size):
    print('EXPERIMENT 2')

    d = 1
    running = True
    
    while(running):
        print('d:', d)
        generator.create_model(d, layer_size, n)
        generator.create_inputs(dataset_size, n, "./generated_dataset.csv")
        print('Dataset generated')  # TEST - EXPERIMENT
        
        start = time.time()
        run_nn_sat("./generated_dataset.csv")
        stop = time.time()
        
        evaluator.create_model("./model.csv")
        evaluator.evaluate_dataset("./generated_dataset.csv")
        
        execution_time = stop - start
        print('Execution time (sec): ', execution_time)
        
        if(execution_time/60 >= 10):
            running = False
        
        d += 1
        print()


#Investigates the influence of d with the number of activated neurons at layer d.
#I.e. If d = 10, how many neurons are activated in that layer?
def experiment3(n, layer_size, dataset_size):
    print('EXPERIMENT 3')

    print('Implement this')


#Given a neural network with d layers, try to synthesize a network with d - 1 layers and see 
#if it still correctly fits the model. Same goes for l.
def experiment4(n, depth, layer_size, dataset_size):
    print('EXPERIMENT 4')
    
    print('d:', d, '\nl: ', layer_size)
    generator.create_model(depth, layer_size, n)
    generator.create_inputs(dataset_size, n, "./generated_dataset.csv")
    print('Dataset generated')  # TEST - EXPERIMENT
    
    run_nn_sat("./generated_dataset.csv")

    evaluator.create_model("./model.csv")
    evaluator.evaluate_dataset("./generated_dataset.csv")


        
#experiment1(2, 4, 100)
experiment2(10, 8, 100)
