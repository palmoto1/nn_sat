import csv
import random
from neuron import Neuron

class DatasetGenerator:


    def __init__(self):
        self.neurons = {}




    def create_model(self, depth, layer_size, string_length):
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

        #g.print_model()
        self.create_input_layer(input)

        last_key = len(self.neurons) - 1

        #print("Evaluate : ")
        #self.print_model()
        #print(self.neurons[last_key][0])
        #print("Last gate:", self.neurons[last_key][0].threshold)
        return self.neurons[last_key][0].get_output() 
    

    def create_input(self, length):
         
        input = ""

        for i in range(length):
            input += random.choice(['0', '1'])


        #print(input)
        #print(self.evaluate(input))
        label = str(self.evaluate(input))

        return label + input

        


    def create_inputs(self, no_of_inputs, input_length, file_path):
        inputs = []
        header = ["header", len(self.neurons) - 2, len(self.neurons[1])] 
         

        for i in range(no_of_inputs):
              inputs.append(self.create_input(input_length))
         

        with open(file_path, 'w') as file:
             writer = csv.writer(file)
             writer.writerow(header)
             writer.writerows(inputs)
             writer.writerow(["end"])

        print(inputs)


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


g.create_model(3, 10, 10)

g.create_inputs(100, 10, "./generated_dataset.csv")


g.print_model()


















# import csv
# import sys
# import random
# from os.path import abspath, dirname, join


# no_of_datasets = int(sys.argv[1])


# def generate_dataset(m, n, threshold):
#     result = []
#     while len(result) < m:
#         s = ''.join(random.choices(['0', '1'], k=n-1))
#         count_ones = s.count('1')
#         if count_ones < threshold:
#             result.append(('0' + s))
#         else:
#             result.append(('1' + s))
    

#     return result


# with open(join(dirname(abspath(__file__)), "dataset.csv"), 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)
#     min_inputs = 2
#     max_inputs = 10

#     for d in range(no_of_datasets):
#         C = 1 # currently assuming only 1 neuron
#         m = random.randint(min_inputs, max_inputs) # generate a random number of input strings from 2 to 10
#         n = random.randint(min_inputs+1, max_inputs) # generate a random number of input bits per string from 2 to 10 + the label
#         max_weigth = n # max value for weight should be the number of bits in an input string
#         threshold = random.randint(1, n-1) # minimum of true bits for an input string to be accepted

#         header = ['header', C, max_weigth]
#         data = generate_dataset(m, n, threshold)

#         # print(data)
#         # print()

#         # write the header
#         writer.writerow(header)

#         # write multiple rows
#         writer.writerows(data)

#         # separating datasets
#         writer.writerow(['end'])
