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
#SBATCH --output=compute_training_thumos_%j.out

module load 2022r2
module load cuda/11.7
module load miniconda3

unset CONDA_SHLVL
source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate action-former

seeds=(357136044 546248239 71714933 626093760 588848963)
for seed in ${seeds[@]}
do
	rm -rf ./ckpt/thumos_i3d_reproduce/*
	srun python ./train.py ./configs/thumos_i3d_training.yaml --output reproduce --seed=$seed
	srun python ./eval.py ./configs/thumos_i3d_training.yaml ./ckpt/thumos_i3d_training_reproduce --seed=$seed
done
conda deactivate
