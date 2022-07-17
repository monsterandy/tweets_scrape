#!/bin/sh

#SBATCH --partition=general-compute --qos=general-compute
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=IB
#SBATCH --mem=2000
# Memory per node specification is in MB. It is optional. 
# The default limit is 3000MB per core.
#SBATCH --job-name="12_vaccine"
#SBATCH --output=ccr_outputs/job_vaccine_12.out
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
python autocommand.py -t vaccine -s 2021-10-01 -e 2021-10-31
python scrape_tweets.py -n vaccine_10
python image_extract.py -n vaccine_10

python autocommand.py -t vaccine -s 2021-11-01 -e 2021-11-30
python scrape_tweets.py -n vaccine_11
python image_extract.py -n vaccine_11

python autocommand.py -t vaccine -s 2021-12-01 -e 2021-12-31
python scrape_tweets.py -n vaccine_12
python image_extract.py -n vaccine_12

module unload python/my-conda
which python
echo "Job end!"
