import csv
import sys
import random
from os.path import abspath, dirname, join


no_of_datasets = int(sys.argv[1])


def generate_dataset(m, n, threshold):
    result = []
    while len(result) < m:
        s = ''.join(random.choices(['0', '1'], k=n-1))
        count_ones = s.count('1')
        if count_ones < threshold:
            result.append(('0' + s))
        else:
            result.append(('1' + s))
    

    return result


with open(join(dirname(abspath(__file__)), "dataset.txt"), 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    min_inputs = 2
    max_inputs = 10

    for d in range(no_of_datasets):
        C = 1 # currently assuming only 1 neuron
        m = random.randint(min_inputs, max_inputs) # generate a random number of input strings from 2 to 10
        n = random.randint(min_inputs+1, max_inputs) # generate a random number of input bits per string from 2 to 10 + the label
        max_weigth = n-1 # max value for weight should be the number of bits in an input string
        threshold = random.randint(1, n-1) # minimum of true bits for an input string to be accepted

        header = [C, max_weigth, threshold]
        data = generate_dataset(m, n, threshold)

        # print(data)
        # print()

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)

        # separating datasets
        writer.writerow([])
