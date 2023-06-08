#!/bin/sh

rm -rf ./results/compute/*

job_id=$(sbatch --parsable run_macs_test.sh)
sleep 5
while [[ $(sacct --job=$job_id | grep -Ec "RUNNING|PENDING") -gt 0 ]]
do
  sleep 1
done

for i in {0..4}
do
  mkdir "./results/compute/compute_$i"
  job_id=$(sbatch --parsable run_memory_time_test.sh $i)

  sleep 5
  while [[ $(sacct --job=$job_id | grep -Ec "RUNNING|PENDING") -gt 0 ]]
  do
    sleep 1
  done
done

