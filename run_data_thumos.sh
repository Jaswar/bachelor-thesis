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
for i in {1..5}
do
	rm -rf ./ckpt/thumos_i3d_reproduce/*
	rm -rf /scratch/jwarchocki/out_datasets/thumos/i3d_features/*
	rm -rf /scratch/jwarchocki/out_datasets/thumos/annotations/*
	python ./data_efficiency.py
	srun python ./train.py ./configs/thumos_i3d.yaml --output reproduce
	srun python ./eval.py ./configs/thumos_i3d.yaml ./ckpt/thumos_i3d_reproduce
done
conda deactivate
