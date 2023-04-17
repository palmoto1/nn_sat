import csv


class Neuron:


    def __init__(self, depth, pos, threshold):
        self.depth = depth
        self.pos = pos
        self.threshold = threshold
        self.predecessors = []


    def add_predecessor(self, neuron):
        self.predecessors.append(neuron)


    def get_output(self):

        if self.depth == 0:
            return self.threshold

        partial_sum = 0
        for n in self.predecessors:
            partial_sum += n.get_output()

        return 1 if partial_sum >= self.threshold else 0
    

    def __str__(self):

        s = "Depth: " + str(self.depth) + " Position: " + str(self.pos) + " Threshold: " + str(self.threshold)
        return s
    


class Network:



    def __init__(self):
        self.neurons = {}


    def create_model(self, file_path):

        self.create_input_layer("1111")

        with open(file_path, "r") as file:
            csvreader = csv.reader(file)


            for row in csvreader:
                weight_variable = row[0]
                if weight_variable != 'end':
                    
                    neuron_data = self.parse_neuron_data(weight_variable) #[key, pos, threshold]

                    key = neuron_data[0]
                    if key not in self.neurons:
                        self.neurons[key] = []

                    pos = neuron_data[1]
                    threshold = neuron_data[2]
                    
                    
                    self.neurons[key].append(Neuron(key, pos, int(threshold))) 


            for key in self.neurons:
                n = int(key)
                if (n != 0):
                    for neuron in self.neurons[key]:
                        neuron.predecessors = self.neurons[str(n - 1)] # do extend if this not works


    def create_input_layer(self, input):

        self.neurons[str(0)] = []

        for i in range(1, len(input)):
            self.neurons[str(0)].append(Neuron(0, i, int(input[i])))


    def evaluate(self):

        last_key = str(len(self.neurons) - 1)

        return self.neurons[last_key][0].get_output()



        

        

    
    def parse_neuron_data(self, s):
        result = []

        i = 6 # we always start parsing from index 6 due to the format
        key = ""

        while s[i] != '_':
            key += s[i]
            i += 1

        result.append(key)

        i += 1
        pos = ""

        while s[i] != '_':
            pos += s[i]
            i += 1

        result.append(pos)

        i += 1
        threshold = ""

        while i < len(s):
            threshold += s[i]
            i += 1

        result.append(threshold)

        return result

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


    

network = Network()

network.create_model("./model.csv")

network.print_model()

print("Evaluation: ", network.evaluate())

        


    