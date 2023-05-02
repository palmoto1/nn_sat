import csv

results = {}
averages = {}

with open("./experiments/experiment2/result/e2-results.csv", "r") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        if row[0] != 'header':
            depth = row[0]
            if depth not in results:
                results[depth] = []
                avg_time = float(row[1])
                results[depth].append(avg_time)    
            else:
                avg_time = float(row[1])
                results[depth].append(avg_time)
                
for key in results.keys():
    key_sum = sum(results[key])
    key_avg = key_sum / len(results[key])
    averages[key] = key_avg
        

for key, value in averages.items():
    print(key, ':', value)