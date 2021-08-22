#!/bin/sh

#SBATCH --partition=general-compute --qos=general-compute
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --constraint=IB
#SBATCH --mem=24000
# Memory per node specification is in MB. It is optional. 
# The default limit is 3000MB per core.
#SBATCH --job-name="04_asianhate"
#SBATCH --output=../ccr_outputs/job_asianhate_04.out
#SBATCH --mail-user=zheyuanm@buffalo.edu
#SBATCH --mail-type=ALL

/usr/bin/hostname
which python

echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory = "$SLURM_SUBMIT_DIR

module use /projects/academic/hongxinh/modulefiles
module load python/my-conda
source /projects/academic/hongxinh/anaconda/etc/profile.d/conda.sh
conda activate tweets
which python
cd ..
cd ..
pwd

echo "Job start!"
python autocommand.py -t asianhate -s 2020-04-01 -e 2020-04-30
python scrape_tweets.py -n asianhate_04
python image_extract.py -n asianhate_04

module unload python/my-conda
which python
echo "Job end!"
