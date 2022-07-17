#!/bin/sh

#SBATCH --partition=general-compute --qos=general-compute
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=IB
#SBATCH --mem=2000
# Memory per node specification is in MB. It is optional. 
# The default limit is 3000MB per core.
#SBATCH --job-name="04_mask"
#SBATCH --output=ccr_outputs/job_mask_04.out
#SBATCH --mail-user=zheyuanm@buffalo.edu
#SBATCH --mail-type=END

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
pwd

echo "Job start!"
python autocommand.py -t mask -s 2021-04-01 -e 2021-04-30
python scrape_tweets.py -n mask-04
python image_extract.py -n mask-04

python autocommand.py -t mask -s 2021-05-01 -e 2021-04-31
python scrape_tweets.py -n mask-05
python image_extract.py -n mask-05

python autocommand.py -t mask -s 2021-06-01 -e 2021-06-30
python scrape_tweets.py -n mask-06
python image_extract.py -n mask-06


module unload python/my-conda
which python
echo "Job end!"
