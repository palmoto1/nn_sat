from nn_sat import *
from data_set_generator import *
from evaluation import *

generator = DatasetGenerator()
evaluator = Evaluation()

#Ensure that the model fits the dataset correctly by increasing the length of n and l with the power 2,
# i.e. n = 8, l = 8 → n = 16, l = 16 → n = 32, l = 32 etc. Max time is set to 10 minutes. d  and size of dataset are constant.
def experiment1(depth, dataset_size):
    
    i = 8
    while(i < 500):
        
        print('i:', i)
        generator.create_model(depth, i, i)
        generator.create_inputs(dataset_size, i, "./generated_dataset.csv")
        
        run_nn_sat()
        
        evaluator.create_model("./model.csv")
        evaluator.evaluate_dataset("./generated_dataset.csv")
        
        i *= 2
        
experiment1(3, 100)