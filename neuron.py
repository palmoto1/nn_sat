class Neuron:


    def __init__(self, depth, pos, threshold):
        self.depth = depth
        self.pos = pos
        self.threshold = threshold
        self.predecessors = []
        self.output = -1


    def add_predecessor(self, neuron):
        self.predecessors.append(neuron)


    def get_output(self):

        if self.depth == 0:
            return self.threshold

        partial_sum = 0
        for n in self.predecessors:
            partial_sum += n.get_output()

        return 1 if partial_sum >= self.threshold else 0
    
    def set_output(self, value):
        self.output = value
    

    def __str__(self):
        s = "Depth: " + str(self.depth) + " Position: " + str(self.pos) + " Threshold: " + str(self.threshold)
        #s = "Depth: " + str(self.depth) + " Position: " + str(self.pos) + " Threshold: " + str(self.threshold) + " Output: " + str(self.get_output()) 
        return s
    