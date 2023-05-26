import csv
import random
from neuron import Neuron

class DatasetGenerator:

    def __init__(self):
        self.neurons = {}
        self.layer_sums = {}
        
        
    # main function for generating a consistent dataset
    def create_dataset(self, depth, layer_size, no_of_inputs, input_length, distribution_threshold, file_path):
        inputs = []

        while not self.check_distribution(inputs, distribution_threshold):   
            inputs = []
            self.create_model(depth, layer_size, input_length)

            for _ in range(no_of_inputs):
              input = self.create_input(input_length)
              inputs.append(input)
              
        header = ["header", depth, layer_size]
        with open(file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(inputs)
            writer.writerow(["end"])


    # checks whether a dataset is distrubuted evenly based on a threshold 
    def check_distribution(self, dataset, threshold):
        if not dataset:
            return False
        
        num_pos = 0
        num_neg = 0

        for item in dataset:
            if(item[0] == '1'):
                num_pos += 1
            else:
                num_neg += 1
        
        spread_neg = num_neg / len(dataset)
        spread_pos = num_pos / len(dataset)
        
        return not spread_neg >= threshold and not spread_pos >= threshold


    # generate a candidate model with randomized gate thresholds
    def create_model(self, depth, layer_size, string_length):
        self.neurons = {}

        for d in range(1, depth + 1):
            for l in range(1, layer_size + 1):
                if d not in self.neurons:
                    self.neurons[d] = []
                if (d == 1):
                    threshold = random.randint(1, string_length)
                else:
                    threshold = random.randint(1, layer_size)

                self.neurons[d].append(Neuron(d, l, threshold))
        
        # output layer
        self.neurons[depth + 1] = []
        threshold = random.randint(1, layer_size)
        self.neurons[depth + 1].append(Neuron(depth + 1, 1, threshold))
       
        for n in self.neurons:
            if (n != 1): # we connect input layer and first hidden layer later
                for neuron in self.neurons[n]:
                    neuron.predecessors = self.neurons[n - 1] 


    # creates the input layer of a model
    def create_input_layer(self, input):
    
        self.neurons[0] = []
          
        for i in range(len(input)):
            self.neurons[0].append(Neuron(0, i + 1, int(input[i])))

        # connect input layer with first hidden layer
        for neuron in self.neurons[1]:
            neuron.predecessors = self.neurons[0]


    # evaluates if an input is accepted or rejected by the model by returning the model output 
    def evaluate(self, input):
        self.create_input_layer(input)

        self.layer_sums = {}
        for d in range(len(self.neurons)):
            self.layer_sums[d] = 0

        for d in range(len(self.neurons)):
            for n in self.neurons[d]:
                if d == 0: # input layer
                    self.layer_sums[0] += n.threshold

                elif self.layer_sums[d-1] >= n.threshold:
                    self.layer_sums[d] += 1
                    

        output_layer = len(self.layer_sums) - 1
        
        return self.layer_sums[output_layer]

    
    # creates a labeled input string to include in a dataset
    def create_input(self, length):
        input = ""
        for _ in range(length):
            input += random.choice(['0', '1'])

        label = str(self.evaluate(input))
        return label + input


    def print_model(self):
        for layer in self.neurons:
            for neuron in self.neurons[layer]:
                pred = "["

                if neuron.predecessors:
                    for i in range(len(neuron.predecessors) - 1):
                        
                        pred += str(neuron.predecessors[i])
                        pred += ","

                

                    pred += str(neuron.predecessors[len(neuron.predecessors) - 1])

                pred += "]"
                print(neuron," Predecessors: ", pred)



# THESE CALLS CAN BE USED FOR TESTING

#g = DatasetGenerator()
#g.create_dataset(11, 8, 100, 10, 0.8, "./generated_dataset.csv")
# g.print_model()

