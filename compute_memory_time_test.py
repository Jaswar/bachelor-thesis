import torch
import argparse
from compute_common import run_command

def main(args):
    torch.manual_seed(args.seed)
    video_lengths = list(range(args.min, args.max + 1, args.increment))
    seeds = torch.randint(0, 10 ** 9, size=(5, len(video_lengths)))

    for repetition in range(5):
        for i, video_length in enumerate(video_lengths):
            iteration = args.iteration
            print(f'Running memory and time measures for '
                  f'iteration={iteration}, repetition={repetition}, video_length={video_length}')
            seed = seeds[repetition][i]
            mem_output_filename = f'results/compute/compute_{iteration}/memory.csv'
            run_command(f'python measure_memory.py --length={video_length} --output={mem_output_filename} --seed={seed}')
            time_output_filename = f'results/compute/compute_{iteration}/time.csv'
            run_command(f'python measure_time.py --length={video_length} --output={time_output_filename} --seed={seed}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform the internal loop for memory and time experiments')
    parser.add_argument('--min', type=int, help='minimum feature length')
    parser.add_argument('--max', type=int, help='maximum feature length')
    parser.add_argument('--increment', type=int, help='feature length increments')
    parser.add_argument('--seed', type=int, default=0, help='the random seed')
    parser.add_argument('--iteration', type=int, help='the current DelftBlue iteration')
    args = parser.parse_args()
    main(args)