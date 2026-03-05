#!/bin/bash
#SBATCH -N 1 # Total number of nodes
#SBATCH -n 16 # Total number of tasks
#SBATCH -c 1 # number of processors per MPI task
#SBATCH -C gpu
#SBATCH -q debug
#SBATCH -J agentic_ai
#SBATCH -t 00:30:00
#SBATCH -A <ACCOUNT>

## Must be executed from the top-level directory

## Usage: sbatch scripts/perlmutter_exec.sh

module load python
module load gpu

VENV_DIR="$SCRATCH/agentic_venv"

if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

export HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxx ## CHANGE THIS LINE

srun --nodes=1 \
    --ntasks-per-node=1 \
    --gres=gpu:4 \
    python darshan_agent_with_context.py --model_id openai/gpt-oss-20b \
    --dataset_dir dataset \
    --log_dir darshan_llm_logs \
    Castro_large.txt