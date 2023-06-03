import statistics

def extract_tIoU(line):
    line = line[1:]
    main_split = line.split(':')
    tIoU = main_split[0].split(' = ')[1]
    return tIoU


def extract_mAP(line):
    line = line[1:]
    main_split = line.split(':')
    metrics = main_split[1]
    mAP = metrics.split(' (%)')[0].split(' = ')[1]
    return float(mAP)


def extract_average_mAP(line):
    line = line.replace('Average mAP: ', '')
    line = line.replace(' (%)', '')
    return float(line)


def extract_run(run):
    lines = run.split('\n')
    mapped = {}
    for line in lines:
        if line.startswith('|'):
            tIoU = extract_tIoU(line)
            mAP = extract_mAP(line)
            mapped[tIoU] = mAP
        elif line.startswith('Average'):
            average_mAP = extract_average_mAP(line)
            mapped['average'] = average_mAP
    return mapped


if __name__ == '__main__':
    ps = ['0_1', '0_2', '0_4', '0_6', '0_8', '1_0']
    parsed = {}
    for p in ps:
        results = {}
        with open(f'results/anet_p_{p}.txt', 'r') as f:
            content = f.read()
        runs = content.split('\n\n')
        for run in runs:
            mapped = extract_run(run)
            for tIoU, mAP in mapped.items():
                if tIoU not in results:
                    results[tIoU] = []
                results[tIoU].append(mAP)
        for tIoU, mAPs in results.items():
            mean = round(statistics.mean(mAPs), 2)
            std = round(statistics.stdev(mAPs), 2)
            if tIoU not in parsed:
                parsed[tIoU] = {}
            parsed[tIoU][p] = (mean, std)

    print(parsed)
    for tIoU, results in parsed.items():
        string = f'mAP@tIou={tIoU}: '
        for p, mAPs in results.items():
            p = float(p.replace('_', '.'))
            string += f'({int(p * 100)}, {round(mAPs[0] - mAPs[1], 2)})'
        print(string)
        string = f'mAP@tIou={tIoU}: '
        for p, mAPs in results.items():
            p = float(p.replace('_', '.'))
            string += f'({int(p * 100)}, {mAPs[0]})'
        print(string)
        string = f'mAP@tIou={tIoU}: '
        for p, mAPs in results.items():
            p = float(p.replace('_', '.'))
            string += f'({int(p * 100)}, {round(mAPs[0] + mAPs[1], 2)})'
        print(string)
        print()
