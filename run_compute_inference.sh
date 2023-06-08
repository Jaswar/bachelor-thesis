#!/bin/sh
#
#SBATCH --job-name="action-former"
#SBATCH --partition=gpu
#SBATCH --time=07:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --account=Education-EEMCS-Courses-CSE3000

module load 2022r2
module load cuda/11.7
module load miniconda3

unset CONDA_SHLVL
source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate action-former

rm -rf ./results/compute_inference/*
srun python ./compute_macs_test.py --min=200 --max=4000 --increment=200
for i in {0..4}
do
  mkdir "./results/compute_inference/compute_$i"
  job_id=$(sbatch --parsable python ./compute_memory_time_test.py --min=200 --max=4000 --increment=200 --iteration=$i)

	sleep 5
	while [[ $(sacct --job=$job_id | grep -Ec "RUNNING|PENDING") -gt 0 ]]
  do
    sleep 1
  done
done

conda deactivate
