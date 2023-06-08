import os
import numpy as np

def process(filename):
    results = {}
    for i in range(5):
        path = os.path.join(f'results/compute/compute_{i}', filename)
        with open(path, 'r') as f:
            content = f.read().split('\n')
            lines = [line for line in content if line != '']
        for line in lines:
            split = line.split(',')
            feat_len = int(split[0])
            metric = float(split[1])
            if feat_len not in results:
                results[feat_len] = []
            results[feat_len].append(metric)
    averaged_results = {}
    for feat_len, metric in results.items():
        averaged_results[feat_len] = (round(np.mean(metric), 2), round(np.std(metric), 2))
    return averaged_results

if __name__ == '__main__':
    with open('results/compute/macs.csv', 'r') as f:
        content = f.read().split('\n')
        lines = [line for line in content if line != '']
    macs_results = {}
    for line in lines:
        split = line.split(',')
        feat_len, gmacs = int(split[0]), float(split[1])
        macs_results[feat_len] = round(gmacs, 2)

    time_results = process('time.csv')
    memory_results = process('memory.csv')
    print(time_results)
    print(memory_results)
    print(macs_results)


