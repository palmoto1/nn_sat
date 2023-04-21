import csv
import re
from neuron import Neuron


class Evaluation:

    def __init__(self):
        self.neurons = {}


    def create_model(self, file_path):
        self.neurons = {}

        with open(file_path, "r") as file:
            csvreader = csv.reader(file)


            for row in csvreader:
                weight_variable = row[0]
                
                    
                key, pos, threshold = self.parse_neuron_data(weight_variable)

                if key not in self.neurons:
                    self.neurons[key] = []

                                    
                self.neurons[key].append(Neuron(key, pos, threshold)) 


            for key in self.neurons:
                n = int(key)
                if (n != 1): # we connect input layer and first hidden layer later
                    for neuron in self.neurons[key]:
                        neuron.predecessors = self.neurons[str(n - 1)] 


    def create_input_layer(self, input):

        self.neurons[str(0)] = []

        for i in range(1, len(input)):
            self.neurons[str(0)].append(Neuron(0, i, int(input[i])))

        # connect input layer with first hidden layer
        for neuron in self.neurons[str(1)]:
                        neuron.predecessors = self.neurons[str(0)]


    def evaluate(self, input):

        self.create_input_layer(input)
        #self.print_model()

        last_key = str(len(self.neurons) - 1)

        return self.neurons[last_key][0].get_output()



    def evaluate_dataset(self, file_path):

        
        with open(file_path, "r") as file:
            csvreader = csv.reader(file)

            result = True
            for input in csvreader:
                if input[0] != 'header' and input[0] != 'end':
                    if(input[0] != str(self.evaluate(input))):
                        result = False
                    #print("Label: ", input[0])
                    #print("Evaluation: ",input[0] == str(self.evaluate(input)))
                    #print()
            print('Evaluation: ', result)
                

        

    
    def parse_neuron_data(self, s):
        pattern = r'^omega_(\d+)_(\d+)_(\d+(?:\.\d+)?)$'
        match = re.match(pattern, s)
        if not match:
            raise ValueError(f"Invalid neuron string: {s}")
        return match.group(1), match.group(2), int(match.group(3))
    


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


    

network = Evaluation()
network.create_model("./model.csv")
network.evaluate_dataset("./generated_dataset.csv")

        


    