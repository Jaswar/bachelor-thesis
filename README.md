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

Although the data should not be in a `./data` folder. Please still create one and make placeholders for THUMOS and ActivityNet
datasets using:
```shell
mkdir data
mkdir data/thumos
mkdir data/anet_1.3
```
The above step is important as later we will make symbolic links from these dataset paths to paths where the data
is actually located.

The experiments also assume the existence of a folder `./results`. You should create that folder using:
```shell
mkdir results
```

## Data efficiency

### Full results

TBD when I get the splits

### Run experiments

The script works by copying the sampled features, the test features, and the annotations to another place. As the first step,
you should thus create a directory `out_datasets` that will hold the copied datasets. This can be done with `mkdir out_datasets`. 

Note that the following procedures are only for one value of `p`. The steps below should be followed for each 
value of `p` that is meant to be tested.

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

4. Create symbolic links from `./data/anet_1.3` to `out_datasets/anet_1.3`. This will allow us to use the default ActivityNet I3D configuration with no changes.
```shell
ln -s <path to out_datasets>/out_datasets/anet_1.3 ./data/anet_1.3
```

5. Run the `run_data_anet.sh` script. The results can be found in the SLURM outputs.
```shell
sbatch run_data_anet.sh
```

## Computational efficiency: Training

As mentioned in the paper, each repetition of the experiment uses the same seeds. The exact
values of these seeds can be found in both `run_cmpute_training_thumos_repetition.sh` and `run_compute_training_anet_repetition.sh`. Those
seeds were obtained by running the `generate_training_seeds.py` script.

### Full results

The full results can be seen in the `./results/compute_training` folder.

### Run experiments

THUMOS:
1. Create a symbolic link from `./data/thumos` to `./datasets/thumos`. This will allow us to use the default THUMOS configuration 
with no changes:
```shell
ln -s ./datasets/thumos ./data/thumos
```
2. In `run_compute_training.sh` make sure the script `run_compute_training_thumos_repetition.sh` is being launched.
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
2. In `run_compute_training.sh` make sure the script `run_compute_training_anet_repetition.sh` is being launched.
3. Run `run_compute_training.sh` as a shell script (**not** with `sbatch`):
```shell
chmod +x run_compute_training.sh
./run_compute_training.sh &
```
This will run the script in the background. The results can be found in the SLURM outputs of the jobs that are launched
by the script.

## Computational efficiency: Inference

As mentioned in the paper, each repetition of the inference time experiment uses the same seeds. The exact values of these seeds
can be found by printing the `seeds` tensor in `compute_time_test.py` and running the experiments.

### Full results

The results can be found in the `results/compute_inference` folder.

### Run experiments

1. Obtain the model trained on the THUMOS'14 dataset, name it `thumos_model.tar` and place it in the `./ckpt` folder.
See the README.md file in the `./ckpt` folder for more details.
2. In the `./results` folder create a subfolder called `compute`:
```shell
mkdir results/compute
```
3. Run the `run_compute_inference.sh` script using:
```shell
chmod +x run_compute_inference.sh
./run_compute_inference.sh &
```
The results will be visible in the `results/compute` folder.