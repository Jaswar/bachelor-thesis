import argparse
import time
import threading
import psutil
from compute_common import load_model, construct_sample
import torch


def monitor_memory(process, result, stop_signal):
    start = time.time()
    while not stop_signal['stop']:
        mb_used = process.memory_info().rss / 1024 ** 2
        current = time.time() - start
        result.append((current, mb_used))
        time.sleep(0.001)


def main(args):
    if args.seed != -1:
        torch.manual_seed(args.seed)
    model = load_model('configs/thumos_i3d.yaml', 'ckpt/thumos_model.tar')
    video_list = construct_sample(args.length, 30, 4, 16)

    result = []
    stop_signal = {'stop': False}
    process = psutil.Process()
    monitor_thread = threading.Thread(target=monitor_memory, args=(process, result, stop_signal))
    monitor_thread.start()
    model(video_list)
    stop_signal['stop'] = True
    monitor_thread.join()

    memory_usage = max(result, key=lambda res: res[1])
    with open(args.output, 'a') as f:
        f.writelines(f'{args.length},{memory_usage[1]}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check the memory usage of the ActionFormer model')
    parser.add_argument('--length', type=int, help='number of features')
    parser.add_argument('--output', type=str, help='where to save the output')
    parser.add_argument('--seed', type=int, default=-1, help='the random seed')
    args = parser.parse_args()
    main(args)

