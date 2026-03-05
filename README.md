# Agentic Framework for analyzing HPC I/O

An **agentic LLM-based framework** that analyzes Darshan logs and generates a structured **textual description of I/O behavior and patterns**.

This tool leverages large language models (LLMs) to interpret Darshan outputs and produce human-readable summaries of HPC application I/O characteristics.

---

## 🚀 Overview

Darshan logs contain detailed performance counters and metadata describing HPC application I/O behavior. However, manually interpreting these logs is often time-consuming and non-trivial.

This framework automates both **analysis** and **evaluation** of I/O behavior by:

- Parsing Darshan logs (`.darshan`, `.txt`, or `.csv`)
- Extracting relevant I/O statistics
- Providing structured contextual information to an LLM
- Generating a structured textual description of the detected I/O pattern
- Storing model outputs and logs for later inspection
- Benchmarking model responses against ground truth labels to measure classification accuracy across I/O patterns (e.g., sequential/random, read/write dominance, I/O scale, transfer sizes)

In addition to generating structured summaries, the framework produces benchmarking artifacts (e.g., `accuracy_summary_<TIMESTAMP>.json` under `LOG_DIR`) that aggregate per-method accuracy scores for systematic comparison and reproducible evaluation.

---

## 📦 Supported Input Formats

The `--dataset_file` argument supports:

| Format      | Description |
|------------|------------|
| `.darshan` | Raw Darshan binary log |
| `.txt`     | Output of `darshan-parser` |
| `.csv`     | Structured CSV format (see `medium_original.csv` for reference) |

The file must be located inside `--dataset_dir`.

---

## 🧠 Model Support

You can use any HuggingFace-compatible LLM, e.g. meta-llama/Llama-3.1-8B-Instruct. Make sure the model is accessible locally or via HuggingFace authentication.

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone <your_repo_url>
cd <your_repo>
```

### 2️⃣ Create the environment

You can create a virtual environment to isolate dependencies and ensure a clean, reproducible execution environment for the Darshan agent framework.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Execution

### 1️⃣ Prepare your dataset

Place your Darshan file inside the dataset directory.

Supported formats:
- `.darshan` - The raw binary Darshan log
- `.txt` — Output of `darshan-parser`  
- `.csv` — Structured CSV file (see `medium_original.csv` for under the dataset directory reference)

Example directory structure:

```
project_root/
│
├── dataset/
│   └── your_log_file.darshan.txt
│
├── src/
│   └── darshan_agent_with_context.py
|   └── ...
│
└── README.md
```


### 2️⃣ Run the agent

#### 📘 Usage

You may now use the script with the following options (See `perlmutter_exec.sh` under scripts directory for reference):

```
usage: darshan_agent_with_context.py dataset_file [-h] 
                                     --model_id MODEL_ID
                                     [--auth_token AUTH_TOKEN]
                                     [--dataset_dir DATASET_DIR]
                                     [--log_dir LOG_DIR]
                                     

Darshan Agentic I/O Description Framework

positional arguments:
  dataset_file          Dataset file located inside dataset_dir.
                        Supported formats: .darshan, .txt, .csv

optional arguments:
  -h, --help            show this help message and exit

  --model_id MODEL_ID   LLM model identifier to load
                        (e.g., meta-llama/Llama-3.1-8B-Instruct)

  --auth_token AUTH_TOKEN
                        Hugging Face API token required to download or
                        access models from the HuggingFace Hub; it can
                        be either passed via CLI or one can export as an environment variable, and the script will automatically read the token:

                        export HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxx

  --dataset_dir DATASET_DIR
                        Path to dataset directory
                        (default: ../dataset)

  --log_dir LOG_DIR     Directory where LLM logs (including    
                        conversations
                        and benchmarking results) and outputs will be stored
                        (default: ../llm_logs)
  ```

## 📊 Benchmarking

We evaluate model performance by measuring accuracy across prompt categories that represent different I/O behaviors and workload characteristics. Each run generates files summarizing LLM performance for these queries.

The evaluation measures how accurately the model classifies:

- Sequential vs. Random I/O patterns  
- Read- vs. Write-dominant workloads  
- Mixed Read/Write behaviors  
- Additional Darshan-derived characteristics (e.g., I/O scale and transfer sizes)

Each benchmark run produces a file named `accuracy_summary_<TIMESTAMP>.json`. 
This file is saved under the directory specified by `LOG_DIR` (provided via the command line; the directory will be created if it 
does not exist).
