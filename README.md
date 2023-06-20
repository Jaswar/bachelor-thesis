# Benchmarking Data and Computational Efficiency of ActionFormer on Temporal Action Localization Tasks

This is the implementation of the paper *Benchmarking Data and Computational Efficiency of ActionFormer on Temporal Action Localization Tasks* by Jan Warchocki.
The repository is based on the official repository of ActionFormer available [here](https://github.com/happyharrycn/actionformer_release).

Below you can find information on how to access full results obtained in the experiments or run the 
experiments on your own. Note that the scripts below were designed to work on the DelftBlue cluster. Small changes
(such as module loading) will need to be done to make the scripts work on different SLURM clusters. Designing scripts
to run on non-SLURM machine can be done based on the scripts in this repository.

## Installation

The preferred way to run these experiments is using a Miniconda environment named `action-former`.
The required dependencies can be found in the INSTALL.md file. If using DelftBlue, make sure to have access to the 
GPU partition and the `miniconda3`, `2022r2`, and `cuda/11.7` modules.

## Prerequisites 

Before any experiments, you should follow the instructions from the ActionFormer repository on downloading datasets. 
Instead of putting the datasets in `./data` folder, please put them in a different folder, for example `./datasets`.


## Data efficiency

### Full results

TBD when I get the splits

### Run experiments

The script works by copying the sampled features, the test features, and the annotations to another place. As the first step,
you should thus create a directory `out_datasets` that will hold the copied datasets. This can be done with `mkdir out_datasets`. 

THUMOS'14:
1. Modify the call to the main method in the `data_efficiency.py` file. First arguments is `p/100%` that should be tested for.
Next, is the path to the directory containing the datasets (for example `./datasets`, **not** `./data`). Third argument is the path to `out_datasets` created earlier. Next three arguments should be "thumos", "validation", and "test" for the THUMOS dataset.
2. In the out directory, create a place for the THUMOS dataset, annotations and i3d features:

```shell
# when in the out_datasets directory
mkdir thumos
cd thumos
mkdir annotations
mkdir i3d_features
```

3. Create symbolic links from `./data/thumos` to `out_datasets/thumos`. This will allow us to use the default THUMOS configuration with no changes.
```shell
ln -s <path to out_datasets>/out_datasets/thumos ./data/thumos
```

4. Run the `run_data_thumos.sh` script. The results can be found in the SLURM outputs.
```shell
sbatch run_data_thumos.sh
```

ActivityNet:
1. Modify the call to the main method in the `data_efficiency.py` file. First arguments is `p/100%` that should be tested for.
Next, is the path to the directory containing the datasets (for example `./datasets`, **not** `./data`). Third argument is the path to `out_datasets` created earlier. Next three arguments should be "anet_1.3", "training", and "validation" for the ActivityNet dataset.
2. In the out directory, create a place for the ActivityNet dataset, annotations and i3d features:
```shell
# when in the out_datasets directory
mkdir anet_1.3
cd anet_1.3
mkdir annotations
mkdir i3d_features
```

3. As the model uses score fusion, copy the scores to `out_datasets/anet_1.3/annotations` with:
```shell
cp ./data/anet_1.3/annotations/cuhk_val_simp_share.json <path to out_datasets>/out_datasets/anet_1.3
```

3. Create symbolic links from `./data/anet_1.3` to `out_datasets/anet_1.3`. This will allow us to use the default ActivityNet I3D configuration with no changes.
```shell
ln -s <path to out_datasets>/out_datasets/anet_1.3 ./data/anet_1.3
```

4. Run the `run_data_anet.sh` script. The results can be found in the SLURM outputs.
```shell
sbatch run_data_anet.sh
```

## Computational efficiency: Training

### Full results

TBD when I finish running ActivityNet

### Run experiments

THUMOS:
1. Create a symbolic link from `./data/thumos` to `./datasets/thumos`. This will allow us to use the default THUMOS configuration 
with no changes:
```shell
ln -s ./datasets/thumos ./data/thumos
```
2. In `run_compute_training.sh` make sure the script `run_compute_training_thumos_repetition.sh` is launched.
3. Run `run_compute_training.sh` as a shell script, not with sbatch:
```shell
chmod +x run_compute_training.sh
./run_compute_training.sh &
```
This will run the script in the background. The results can be found in the SLURM outputs of the jobs that are launched
by the script.

ActivityNet:
1. Create a symbolic link from `./data/anet_1.3` to `./datasets/anet_1.3`. This will allow us to use the default ActivityNet configuration 
with no changes:
```shell
ln -s ./datasets/anet_1.3 ./data/anet_1.3
```
2. In `run_compute_training.sh` make sure the script `run_compute_training_anet_repetition.sh` is launched.
3. Run `run_compute_training.sh` as a shell script (**not** with `sbatch`):
```shell
chmod +x run_compute_training.sh
./run_compute_training.sh &
```
This will run the script in the background. The results can be found in the SLURM outputs of the jobs that are launched
by the script.
