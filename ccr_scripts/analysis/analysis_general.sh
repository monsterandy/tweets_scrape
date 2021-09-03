#!/bin/sh

#SBATCH --partition=general-compute --qos=general-compute
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem=8000
# Memory per node specification is in MB. It is optional. 
# The default limit is 3000MB per core.
#SBATCH --job-name="analysis_general"
#SBATCH --output=ccr_outputs/analysis/analysis_general.out
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
python analysis.py -n general_cleaned -c csv_data_general

module unload python/my-conda
which python
echo "Job end!"