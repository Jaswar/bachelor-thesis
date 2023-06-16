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
    print()

    string_lower_time = ''
    string_time = ''
    string_upper_time = ''
    for feature_length, inference_time in time_results.items():
        string_lower_time += f'({feature_length}, {round(inference_time[0] - inference_time[1], 2)})'
        string_time += f'({feature_length}, {inference_time[0]})'
        string_upper_time += f'({feature_length}, {round(inference_time[0] + inference_time[1], 2)})'
    print(string_lower_time)
    print(string_time)
    print(string_upper_time)
    print()

    max_macs = 8200
    string_utilization_lower = ''
    string_utilization = ''
    string_utilization_upper = ''
    for feature_length, gmacs in macs_results.items():
        inference_time = time_results[feature_length][0]
        time_std = time_results[feature_length][1]

        lower_gmacs_per_second = gmacs / (inference_time + time_std) * 1000
        gmacs_per_second = gmacs / inference_time * 1000
        upper_gmacs_per_second = gmacs / (inference_time - time_std) * 1000
        utilization_lower = round(lower_gmacs_per_second / max_macs * 100, 2)
        utilization = round(gmacs_per_second / max_macs * 100, 2)  # value expressed in percentages
        utilization_upper = round(upper_gmacs_per_second / max_macs * 100, 2)
        string_utilization_lower += f'({feature_length}, {utilization_lower})'
        string_utilization += f'({feature_length}, {utilization})'
        string_utilization_upper += f'({feature_length}, {utilization_upper})'
    print(string_utilization_lower)
    print(string_utilization)
    print(string_utilization_upper)
    print()

    string_memory = ''
    for feature_length, memory in memory_results.items():
        string_memory += f'({feature_length}, {memory[0]})'
    print(string_memory)
    print()

    string_gmacs = ''
    for feature_length, gmacs in macs_results.items():
        string_gmacs += f'({feature_length}, {gmacs})'
    print(string_gmacs)
