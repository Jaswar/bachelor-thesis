import json

if __name__ == '__main__':
    with open('../datasets/anet_1.3/annotations/anet1.3_i3d_filtered.json', 'r') as f:
        content = f.read()
    data = json.loads(content)
    single_instance = []
    multi_instance = []
    all_labels = {}
    subsets = {}
    for vid in data['database']:
        subset = data['database'][vid]['subset']
        if subset not in subsets:
            subsets[subset] = 0
        subsets[subset] += 1
        annotations = data['database'][vid]['annotations']
        labels = set()
        for annotation in annotations:
            labels.add(annotation['label'])
        # print(vid, labels, len(annotations))
        for label in labels:
            if label not in all_labels:
                all_labels[label] = {'multi': 0, 'single': 0}
        if len(labels) > 1:
            for label in labels:
                all_labels[label]['multi'] += 1
        else:
            label = list(labels)[0]
            all_labels[label]['single'] += 1
    print(subsets)
    sums = sum(subsets[s] for s in subsets)
    print([subsets[s] / sums for s in subsets])
    lines = ['action,multi,single\n']
    for label in all_labels:
        multi = all_labels[label]['multi']
        single = all_labels[label]['single']
        lines.append(f'{label},{multi},{single}\n')

    with open('output.csv', 'w') as f:
        f.writelines(lines)
