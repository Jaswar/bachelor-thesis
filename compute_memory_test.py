import argparse
from compute_common import run_command


def main(args):
    video_lengths = list(range(args.min, args.max + 1, args.increment))
    for video_length in video_lengths:
        print(f'Running memory test for video_length={video_length}')
        run_command(f'python measure_memory.py --length={video_length} --output=results/compute/memory.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform the internal loop for memory experiments')
    parser.add_argument('--min', type=int, help='minimum feature length')
    parser.add_argument('--max', type=int, help='maximum feature length')
    parser.add_argument('--increment', type=int, help='feature length increments')
    args = parser.parse_args()
    main(args)