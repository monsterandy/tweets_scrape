#!/bin/sh

#SBATCH --partition=general-compute --qos=general-compute
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=IB
#SBATCH --mem=2000
# Memory per node specification is in MB. It is optional. 
# The default limit is 3000MB per core.
#SBATCH --job-name="08_ageism"
#SBATCH --output=ccr_outputs/job_ageism_08.out
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
python autocommand.py -t ageism -s 2021-07-01 -e 2021-07-31
python scrape_tweets.py -n ageism_07
python image_extract.py -n ageism-07

python autocommand.py -t ageism -s 2021-08-01 -e 2021-08-31
python scrape_tweets.py -n ageism-08
python image_extract.py -n ageism-08

python autocommand.py -t ageism -s 2021-09-01 -e 2021-09-30
python scrape_tweets.py -n ageism-09
python image_extract.py -n ageism-09


module unload python/my-conda
which python
echo "Job end!"
