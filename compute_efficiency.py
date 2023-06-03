import os
import torch

def run_command(command):
    os.system(f'conda run -n action-former {command}')


def make_dirs(num_external_repetitions):
    root_path = os.path.join('results', 'compute')
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    for i in range(num_external_repetitions):
        repetition_path = os.path.join(root_path, f'compute_{i}')
        if not os.path.exists(repetition_path):
            os.mkdir(repetition_path)


if __name__ == '__main__':
    num_internal_repetitions = 5
    num_external_repetitions = 5
    video_lengths = list(range(576, 2305, 576))  # Use 144 in the end
    # Fix the seeds for each external repetition
    torch.manual_seed(0)
    seeds = torch.randint(0, 10 ** 9, size=(num_internal_repetitions, len(video_lengths)))

    make_dirs(num_external_repetitions)
    for video_length in video_lengths:
        print(f'Running MACs counter for {video_length=}')
        run_command(f'python measure_macs.py --length={video_length} --output=results/compute/macs.csv')

    for ext_repetition in range(num_external_repetitions):
        for int_repetition in range(num_internal_repetitions):
            for i, video_length in enumerate(video_lengths):
                print(f'Running memory and time measures for {int_repetition=}, {video_length=}')
                seed = seeds[int_repetition][i]
                mem_output_filename = f'results/compute/compute_{ext_repetition}/memory.csv'
                run_command(f'python measure_memory.py --length={video_length} --output={mem_output_filename} --seed={seed}')
                time_output_filename = f'results/compute/compute_{ext_repetition}/time.csv'
                run_command(f'python measure_time.py --length={video_length} --output={time_output_filename} --seed={seed}')

