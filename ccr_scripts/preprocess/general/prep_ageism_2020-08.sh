#!/bin/sh

#SBATCH --partition=general-compute --qos=general-compute
#SBATCH --time=18:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem=8000
# Memory per node specification is in MB. It is optional. 
# The default limit is 3000MB per core.
#SBATCH --job-name="20-08_ageism_prep"
#SBATCH --output=ccr_outputs/preprocess/general/prep_ageism_2020-08.out
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
which tesseract
pwd

echo "Job start!"
python preprocess.py -n ageism_2020-08

module unload python/my-conda
which python
echo "Job end!"
