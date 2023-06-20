import json


def isSubsetSum(se, n, su):
    # Base Cases
    if (su == 0):
        return True
    if (n == 0 and su != 0):
        return False

    # If last element is greater than
    # sum, then ignore it
    if (se[n - 1] > su):
        return isSubsetSum(se, n - 1, su)

        # else, check if sum can be obtained
    # by any of the following
    # (a) including the last element
    # (b) excluding the last element
    return isSubsetSum(se, n - 1, su) or isSubsetSum(se, n - 1, su - se[n - 1])


if __name__ == '__main__':
    with open('../../datasets/anet_1.3/annotations/anet1.3_i3d_filtered.json', 'r') as f:
        content = f.read()
    data = json.loads(content)
    single_instance = []
    multi_instance = []
    all_labels = {}
    subsets = {}
    class_instances = {}
    num_instances = 0
    for vid in data['database']:
        subset = data['database'][vid]['subset']
        if subset not in subsets:
            subsets[subset] = 0
        subsets[subset] += 1
        annotations = data['database'][vid]['annotations']
        instances = {}
        for annotation in annotations:
            label = annotation['label']
            if label not in instances:
                instances[label] = 0
            instances[label] += 1
        for instance, num in instances.items():
            if instance not in class_instances:
                class_instances[instance] = []
            class_instances[instance].append(num)
        if subset.lower() == 'training':
            num_instances += len(annotations)
        # labels = set()
        # for annotation in annotations:
        #     labels.add(annotation['label'])
        # # print(vid, labels, len(annotations))
        # for label in labels:
        #     if label not in all_labels:
        #         all_labels[label] = {'multi': 0, 'single': 0}
        # if len(labels) > 1:
        #     for label in labels:
        #         all_labels[label]['multi'] += 1
        # else:
        #     label = list(labels)[0]
        #     all_labels[label]['single'] += 1
    print(num_instances)
    print(num_instances / 20)
    print(len(class_instances))
    # print(class_instances)
    # for i in range(1, 68):
    #     has_subsets = True
    #     for cls, instances in class_instances.items():
    #         if not isSubsetSum(instances, len(instances), i):
    #             has_subsets = False
    #             break
    #     print(f'For {i=}, {has_subsets=}')
    # print(subsets)
    # sums = sum(subsets[s] for s in subsets)
    # print([subsets[s] / sums for s in subsets])
    # lines = ['action,multi,single\n']
    # for label in all_labels:
    #     multi = all_labels[label]['multi']
    #     single = all_labels[label]['single']
    #     lines.append(f'{label},{multi},{single}\n')

    # with open('output.csv', 'w') as f:
    #     f.writelines(lines)
