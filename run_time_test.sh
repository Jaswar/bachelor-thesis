#!/bin/sh
#
#SBATCH --job-name="action-former"
#SBATCH --partition=gpu
#SBATCH --time=02:00:00
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

srun python ./compute_time_test.py --min=200 --max=3000 --increment=200 --iteration=$1

conda deactivate