#!/bin/sh

for i in {0..4}
do
  # replace with run_compute_training_anet_repetition.sh for the ActivityNet dataset
  job_id=$(sbatch --parsable run_compute_training_thumos_repetition.sh)

  sleep 5
  while [[ $(sacct --job=$job_id | grep -Ec "RUNNING|PENDING") -gt 0 ]]
  do
    sleep 1
  done
done