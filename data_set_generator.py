import csv
import random
import decimal
from neuron import Neuron

class DatasetGenerator:


    def __init__(self):
        self.neurons = {}
        
    def create_dataset(self, depth, layer_size, no_of_inputs, input_length, file_path):
        inputs = []

        while not self.check_distribution(inputs, 0.8):
            inputs = []
            self.create_model(depth, layer_size, input_length)

            for i in range(no_of_inputs):
              inputs.append(self.create_input(input_length))
              
        header = ["header", len(self.neurons) - 2, len(self.neurons[1])]
        with open(file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(inputs)
            writer.writerow(["end"])

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
        self.neurons[depth +1] = []
        threshold = random.randint(1, layer_size)
        self.neurons[depth + 1].append(Neuron(depth + 1, 1, threshold))
       

        for n in self.neurons:
            if (n != 1): # we connect input layer and first hidden layer later
                for neuron in self.neurons[n]:
                    neuron.predecessors = self.neurons[n - 1] 


    def create_input_layer(self, input):
        self.neurons[0] = []
        #print(input)
        for i in range(len(input)):
            self.neurons[0].append(Neuron(0, i + 1, int(input[i])))

        # connect input layer with first hidden layer
        for neuron in self.neurons[1]:
            neuron.predecessors = self.neurons[0]


    def evaluate(self, input):
        self.create_input_layer(input)

        last_key = len(self.neurons) - 1
        return self.neurons[last_key][0].get_output() 
    

    def create_input(self, length):
        input = ""

        for i in range(length):
            input += random.choice(['0', '1'])

        label = str(self.evaluate(input))

        return label + input

        


    
    
    #For overnight dataset generation
    def generate_datasets_by_depth(self, layer_size, n, dataset_size, no_datasets):
        d = 1
        while(d <= no_datasets):
            print(d)
            file_path = "./datasets/generated_dataset" + str(d) + ".csv"
            #self.create_model(d, layer_size, n)
            #self.create_inputs(dataset_size, n, file_path)
            self.create_dataset(d, layer_size, dataset_size, n, file_path)
            d += 1


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




g = DatasetGenerator()
#g.create_dataset(3, 8, 10, 8, "./generated_dataset.csv")
g.generate_datasets_by_depth(8, 10, 25, 50)
# g.create_model(3, 8, 8)
# g.create_inputs(100, 8, "./generated_dataset.csv")
# g.print_model()

