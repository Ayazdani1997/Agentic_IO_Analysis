

import os
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = "SOMETHING" IMPORTANT, THIS LINE MUST BE CONFIGURED

# NOTE: This snippet was adapted from the ION project:
# https://github.com/DIR-LAB/ION

DARSHAN_MODULES = {
    "POSIX": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "POSIX_*": "POSIX operation counters. Possible operations include: READS, WRITES, OPENS, SEEKS, STATS, MMAPS, SYNCS, FILENOS, DUPS",
            "POSIX_RENAME_SOURCES/TARGETS": "total count file was source or target of a rename operation",
            "POSIX_RENAMED_FROM": "Darshan record ID of the first rename source, if file was a rename target",
            "POSIX_MODE": "mode that file was opened in.",
            "POSIX_BYTES_*": "total bytes read or written.",
            "POSIX_MAX_BYTE_*": "highest offset byte read or written.",
            "POSIX_CONSEC_*": "number of exactly adjacent reads and writes.",
            "POSIX_SEQ_*": "number of reads and writes from increasing offsets.",
            "POSIX_RW_SWITCHES": "number of times access alternated between read and write.",
            "POSIX_*_ALIGNMENT": "memory and file alignment.",
            "POSIX_*_NOT_ALIGNED": "number of reads and writes that were misaligned.",
            "POSIX_MAX_*_TIME_SIZE": "size of the slowest read and write operations.",
            "POSIX_SIZE_*_*": "histogram of read and write access sizes.",
            "POSIX_STRIDE*_STRIDE": "the four most common strides detected.",
            "POSIX_STRIDE*_COUNT": "count of the four most common strides.",
            "POSIX_ACCESS*_ACCESS": "the four most common access sizes.",
            "POSIX_ACCESS*_COUNT": "count of the four most common access sizes.",
            "POSIX_*_RANK": "rank of the processes that were the fastest and slowest at I/O (for shared files).",
            "POSIX_*_RANK_BYTES": "bytes transferred by the fastest and slowest ranks (for shared files).",
            "POSIX_F_*_START_TIMESTAMP": "timestamp of first open/read/write/close.",
            "POSIX_F_*_END_TIMESTAMP": "timestamp of last open/read/write/close.",
            "POSIX_F_READ/WRITE/META_TIME": "cumulative time spent in read, write, or metadata operations.",
            "POSIX_F_MAX_*_TIME": "duration of the slowest read and write operations.",
            "POSIX_F_*_RANK_TIME": "fastest and slowest I/O time for a single rank (for shared files).",
            "POSIX_F_VARIANCE_RANK_*": "variance of total I/O time and bytes moved for all ranks (for shared files).",
        },
        "warnings": "POSIX_OPENS counter includes both POSIX_FILENOS and POSIX_DUPS counts. POSIX counters related to file offsets may be incorrect if a file is simultaneously accessed by both POSIX and STDIO (e.g., using fileno()). Affected counters include: MAX_BYTE_{READ|WRITTEN}, CONSEC_{READS|WRITES}, SEQ_{READS|WRITES}, {MEM|FILE}_NOT_ALIGNED, STRIDE*_STRIDE."
    },
    "MPI-IO": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "MPIIO_INDEP_*": "MPI independent operation counts.",
            "MPIIO_COLL_*": "MPI collective operation counts.",
            "MPIIO_SPLIT_*": "MPI split collective operation counts.",
            "MPIIO_NB_*": "MPI non-blocking operation counts.",
            "READS,WRITES,OPENS": "types of operations at MPI-IO layer.",
            "MPIIO_SYNCS": "MPI file sync operation counts.",
            "MPIIO_HINTS": "number of times MPI hints were used.",
            "MPIIO_VIEWS": "number of times MPI file views were used.",
            "MPIIO_MODE": "MPI-IO access mode that file was opened with.",
            "MPIIO_BYTES_*": "total bytes read and written at MPI-IO layer.",
            "MPIIO_RW_SWITCHES": "number of times access alternated between read and write at MPI-IO layer.",
            "MPIIO_MAX_*_TIME_SIZE": "size of the slowest read and write operations at MPI-IO layer.",
            "MPIIO_SIZE_*_AGG_*": "histogram of MPI datatype total sizes for read and write operations.",
            "MPIIO_ACCESS*_ACCESS": "the four most common total access sizes at MPI-IO layer.",
            "MPIIO_ACCESS*_COUNT": "count of the four most common total access sizes.",
            "MPIIO_*_RANK": "rank of the processes that were the fastest and slowest at I/O (for shared files) at MPI-IO layer.",
            "MPIIO_*_RANK_BYTES": "total bytes transferred at MPI-IO layer by the fastest and slowest ranks (for shared files).",
            "MPIIO_F_*_START_TIMESTAMP": "timestamp of first MPI-IO open/read/write/close.",
            "MPIIO_F_*_END_TIMESTAMP": "timestamp of last MPI-IO open/read/write/close.",
            "MPIIO_F_READ/WRITE/META_TIME": "cumulative time spent in MPI-IO read, write, or metadata operations.",
            "MPIIO_F_MAX_*_TIME": "duration of the slowest MPI-IO read and write operations.",
            "MPIIO_F_*_RANK_TIME": "fastest and slowest I/O time for a single rank (for shared files) at MPI-IO layer.",
            "MPIIO_F_VARIANCE_RANK_*": "variance of total I/O time and bytes moved for all ranks (for shared files) at MPI-IO layer."
        },

    },
    "HDF5": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "H5F_OPENS": "HDF5 file open/create operation counts.",
            "H5F_FLUSHES": "HDF5 file flush operation counts.",
            "H5F_USE_MPIIO": "flag indicating whether MPI-IO was used to access this file.",
            "H5F_F_*_START_TIMESTAMP": "timestamp of first HDF5 file open/close.",
            "H5F_F_*_END_TIMESTAMP": "timestamp of last HDF5 file open/close.",
            "H5F_F_META_TIME": "cumulative time spent in HDF5 metadata operations."
        }
    },
    "BGQ": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "BGQ_CSJOBID": "BGQ control system job ID.",
            "BGQ_NNODES": "number of BGQ compute nodes for this job.",
            "BGQ_RANKSPERNODE": "number of MPI ranks per compute node.",
            "BGQ_DDRPERNODE": "size in MB of DDR3 per compute node.",
            "BGQ_INODES": "number of BGQ I/O nodes for this job.",
            "BGQ_*NODES": "dimension of A, B, C, D, & E dimensions of torus.",
            "BGQ_TORUSENABLED": "which dimensions of the torus are enabled.",
            "BGQ_F_TIMESTAMP": "timestamp when the BGQ data was collected."
        }
    },
    "STDIO": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "STDIO_*": "STDIO operation counts. Possible operations include: OPENS, FDOPENS, WRITES, READS, SEEKS, FLUSHES",
            "STDIO_BYTES_*": "total bytes read and written.",
            "STDIO_MAX_BYTE_*": "highest offset byte read and written.",
            "STDIO_*_RANK": "rank of the processes that were the fastest and slowest at I/O (for shared files).",
            "STDIO_*_RANK_BYTES": "bytes transferred by the fastest and slowest ranks (for shared files).",
            "STDIO_F_*_START_TIMESTAMP": "timestamp of the first call to that type of function.",
            "STDIO_F_*_END_TIMESTAMP": "timestamp of the completion of the last call to that type of function.",
            "STDIO_F_*_TIME": "cumulative time spent in different types of functions.",
            "STDIO_F_*_RANK_TIME": "fastest and slowest I/O time for a single rank (for shared files).",
            "STDIO_F_VARIANCE_RANK_*": "variance of total I/O time and bytes moved for all ranks (for shared files)."
        }
    },
    "LUSTRE": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "LUSTRE_OSTS": "number of OSTs (Object Storage Targets) across the entire file system.",
            "LUSTRE_MDTS": "number of MDTs (Metadata Targets) across the entire file system.",
            "LUSTRE_STRIPE_OFFSET": "OST ID offset specified when the file was created.",
            "LUSTRE_STRIPE_SIZE": "stripe size for the file in bytes.",
            "LUSTRE_STRIPE_WIDTH": "number of OSTs over which the file is striped.",
            "LUSTRE_OST_ID_*": "indices of OSTs over which the file is striped."
        }
    },
    "DXT": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "file_id": "unique ID assigned to each file",
            "file_name": "Path and name of the file",
            "api": "I/O library being used",
            "rank": "MPI rank from which the operation was called",
            "operation": "type of I/O call ('read', 'write', 'open', 'stat')",
            "segment": "portion of a file that is accessed during an I/O operation",
            "offset": "position within a file where a particular I/O operation begins",
            "size": "amount of data read from or written to a file during an I/O operation in bytes",
            "start": "unix timestamp of the start of the I/O operation",
            "end": "unix timestamp of the end of the I/O operation",
            "ost": "lustre OST used by the I/O operation",
            "consec": "boolean to indicate if current offset is greater than the previous offset+size",
            "seq": "boolean to indicate if current offset is equal to the previous offset + size"
        }
    },
    "MDHIM": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "MDHIM_PUTS": "number of 'mdhim_put' function calls.",
            "MDHIM_GETS": "number of 'mdhim_get' function calls.",
            "MDHIM_SERVERS": "how many mdhim servers were utilized.",
            "MDHIM_F_PUT_TIMESTAMP": "timestamp of the first call to function 'mdhim_put'.",
            "MDHIM_F_GET_TIMESTAMP": "timestamp of the first call to function 'mdhim_get'.",
            "MDHIM_SERVER_N": "how many operations were sent to this server."
        }
    },
    "NULL": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "NULL_FOOS": "number of 'foo' function calls.",
            "NULL_FOO_MAX_DAT": "maximum data value set by calls to 'foo'.",
            "NULL_F_FOO_TIMESTAMP": "timestamp of the first call to function 'foo'.",
            "NULL_F_FOO_MAX_DURATION": "timer indicating duration of call to 'foo' with max NULL_FOO_MAX_DAT value."
        }

    },
    "PNETCDF": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "PNETCDF_VAR_OPENS": "PnetCDF variable define/inquire operation counts.",
            "PNETCDF_VAR_INDEP_READS": "PnetCDF variable independent read operation counts.",
            "PNETCDF_VAR_INDEP_WRITES": "PnetCDF variable independent write operation counts.",
            "PNETCDF_VAR_COLL_READS": "PnetCDF variable collective read operation counts.",
            "PNETCDF_VAR_COLL_WRITES": "PnetCDF variable collective write operation counts.",
            "PNETCDF_VAR_NB_READS": "PnetCDF variable nonblocking read operation counts.",
            "PNETCDF_VAR_NB_WRITES": "PnetCDF variable nonblocking write operation counts.",
            "PNETCDF_VAR_BYTES_*": "total bytes read and written at PnetCDF variable layer.",
            "PNETCDF_VAR_RW_SWITCHES": "number of times access alternated between read and write at PnetCDF layer.",
            "PNETCDF_VAR_PUT_VAR*": "number of calls to ncmpi_put_var* APIs (var, var1, vara, vars, varm, varn, vard).",
            "PNETCDF_VAR_GET_VAR*": "number of calls to ncmpi_get_var* APIs (var, var1, vara, vars, varm, varn, vard).",
            "PNETCDF_VAR_IPUT_VAR*": "number of calls to ncmpi_iput_var* APIs (var, var1, vara, vars, varm, varn).",
            "PNETCDF_VAR_IGET_VAR*": "number of calls to ncmpi_iget_var* APIs (var, var1, vara, vars, varm, varn).",
            "PNETCDF_VAR_BPUT_VAR*": "number of calls to ncmpi_bput_var* APIs (var, var1, vara, vars, varm, varn).",
            "PNETCDF_VAR_MAX_*_TIME_SIZE": "size of the slowest read and write operations at PnetCDF layer.",
            "PNETCDF_VAR_SIZE_*_AGG_*": "histogram of PnetCDF total access sizes for read and write operations.",
            "PNETCDF_VAR_ACCESS*_*": "the four most common total accesses, in terms of size and length/stride (in last 5 dimensions) at PnetCDF layer.",
            "PNETCDF_VAR_ACCESS*_COUNT": "count of the four most common total access sizes at PnetCDF layer.",
            "PNETCDF_VAR_NDIMS": "number of dimensions in the variable.",
            "PNETCDF_VAR_NPOINTS": "number of points in the variable.",
            "PNETCDF_VAR_DATATYPE_SIZE": "size of each variable element at PnetCDF layer.",
            "PNETCDF_VAR_*_RANK": "rank of the processes that were the fastest and slowest at I/O (for shared datasets) at PnetCDF layer.",
            "PNETCDF_VAR_*_RANK_BYTES": "total bytes transferred at PnetCDF layer by the fastest and slowest ranks (for shared datasets).",
            "PNETCDF_VAR_F_*_START_TIMESTAMP": "timestamp of first PnetCDF variable open/read/write/close.",
            "PNETCDF_VAR_F_*_END_TIMESTAMP": "timestamp of last PnetCDF variable open/read/write/close.",
            "PNETCDF_VAR_F_READ/WRITE/META_TIME": "cumulative time spent in PnetCDF read, write, or metadata operations.",
            "PNETCDF_VAR_F_MAX_*_TIME": "duration of the slowest PnetCDF read and write operations.",
            "PNETCDF_VAR_F_*_RANK_TIME": "fastest and slowest I/O time for a single rank (for shared datasets) at PnetCDF layer.",
            "PNETCDF_VAR_F_VARIANCE_RANK_*": "variance of total I/O time and bytes moved for all ranks (for shared datasets) at PnetCDF layer.",
            "PNETCDF_VAR_FILE_REC_ID": "Darshan file record ID of the file the variable belongs to."
        }
    },

    "HEATMAP": {
        "column_description": {
            "module": "module responsible for this I/O record.",
            "rank": "MPI rank. -1 indicates that the file is shared across all processes and statistics are aggregated.",
            "record id": "hash of the record's file path",
            "file name": "full file path for the record.",
            "mount pt": "mount point that the file resides on.",
            "fs type": "type of file system that the file resides on.",
            "HEATMAP_F_BIN_WIDTH_SECONDS": "time duration of each heatmap bin.",
            "HEATMAP_READ_BIN_*": "number of bytes read within specified heatmap bin.",
            "HEATMAP_WRITE_BIN_*": "number of bytes written within specified heatmap bin."
        }
    },
}

import pandas as pd

import os
import argparse

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import sys
from transformers import pipeline
import os
from datetime import datetime
from langchain_community.llms import HuggingFacePipeline
from io import StringIO
import json
import numpy as np
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from benchmarking import report_accuracy_shared_independent
from benchmarking import report_accuracy_read_write
from benchmarking import print_accuracy_stat
from benchmarking import report_accuracy_sequential_random
from benchmarking import report_accuracy_huge_small
from benchmarking import report_accuracy_summarization
from benchmarking import extract_last_json

import subprocess
from pathlib import Path

'''
    Darshan logs are sparse; the function extracts the
    counters that are important (non-zero)

    Precondition: Each list item is a tuple of the dataset, and its associated darshan log path. The datasets are organized into a collection of rows
    ; the important columns for each row are the the following:

        - `module`: The I/O interface through which the I/O operation is carried out
        - `counter`: The Darshan counter representing a metric (e.g. POSIX_WRITES denoting the number of POSIX write ops)
        - `value`: The value for the Darshan counter
        - `recordid`: The id of the file being the target of the I/O
        - `filename`: The path to the file being the target of the I/O
        

    Returns: the refined list with the zero counters discarded.

'''

def extract_important_counters(darshan_dataframes):
    refined_darshan_dataframes = []
    for darshan_dataset in darshan_dataframes:
        df = pd.DataFrame()
        # print(darshan_dataset)
        df = darshan_dataset[1].loc[
                                        (darshan_dataset[1]['value'] != 0) &
                                        (darshan_dataset[1]['value'].notna())
                                    ].copy()
        refined_darshan_dataframes.append((darshan_dataset[0], df))
    return refined_darshan_dataframes


'''
Function to read the darshan text file and convert it into a CSV format; 
it also removes NaN values
'''
def read_darshan_text_blocks(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize a list to store dataframes
    dfs = []
    current_block = ""
    block_seen = False

    # Iterate through lines to process text blocks
    idx = 0
    for line in lines:
        # print(line)
        if line.startswith("#<module>"):
            # print(">>>>>>>>>>>>>>>>>>> start ")
            # print(line)
            # print(current_block.strip())
            # if current_block.strip() != "":
            #     # Process the current block and append it to the list of dataframes
            #     # dfs.append(process_text_block(current_block))
            current_block = ""
            block_seen = True
        if block_seen:
            # print(line)
            current_block += line

        # Process the last block if it exists
        # print(f"{idx + 1}:length={len(line)}:{line}")
        if (len(line) == 1) and block_seen:
            # print(">>>>>>>>>>>>>>>>>>> end ")
            dfs.append(preprocess_darshan_blocks(current_block))
            block_seen = False
            # current_block = ""
        idx += 1
    if block_seen:
        # print(">>>>>>>>>>>>>>>>>>> end ")
        dfs.append(preprocess_darshan_blocks(current_block))
        block_seen = False
    # Concatenate all dataframes
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return None

'''
    Preprocessing the darshan blocks, e.g. removing NaN values
'''
def preprocess_darshan_blocks(text_block):
    # Replace any "UNKNOWN" with NaN
    text_block = text_block.replace("UNKNOWN", "NaN")
    
    # print(text_block)

    # Use StringIO to simulate a file-like object
    data = StringIO(text_block)

    # Read the dataframe, skip the first character '#' in the header
    df = pd.read_csv(data, sep='\t', na_values='NaN')
    
    # Clean up the column headers
    df.columns = df.columns.str.replace(r'[<>#]', '', regex=True).str.replace(' ', '')
    # print(len(df))

    return df


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze logs using a specified LLM model."
    )

    parser.add_argument(
        "--model_id",
        type=str,
        required=True,
        help="LLM model identifier to load (e.g., meta-llama/Llama-3-8B)"
    )

    parser.add_argument(
        "--dataset_dir",
        type=str,
        default="../dataset",
        help="Path to the dataset directory (default: ../dataset)"
    )

    parser.add_argument(
        "dataset_file",
        type=str,
        help=(
            "Dataset file name inside dataset_dir. "
            "The file can be either a .txt file (Darshan-parser output) "
            "or a .csv file (see medium_original.csv for format reference)."
        )
    )

    parser.add_argument(
        "--log_dir",
        type=str,
        default="../llm_logs",
        help="Directory where LLM logs will be stored"
    )

    parser.add_argument(
        "--auth_token",
        type=str,
        help="Hugging Face API token used to access private or gated models on the HuggingFace Hub."
)

    return parser.parse_args()


args = parse_args()


import os
import torch

print("CUDA_VISIBLE_DEVICES:", os.environ.get("CUDA_VISIBLE_DEVICES"))
print("Detected CUDA device count:", torch.cuda.device_count())

token = args.auth_token or os.environ.get("HUGGINGFACEHUB_API_TOKEN")

if token is None:
    raise ValueError(
        "HuggingFace token not provided. Use --auth_token or export HUGGINGFACEHUB_API_TOKEN."
    )

os.environ["HUGGINGFACEHUB_API_TOKEN"] = token

# Paths
dataset_dir = os.path.abspath(args.dataset_dir)
dataset_path = os.path.join(dataset_dir, args.dataset_file)
log_dir = os.path.abspath(args.log_dir)

# Model
model_id = args.model_id

print("Model ID:", model_id)
print("Dataset path:", dataset_path)
print("Base dir:", log_dir)


if dataset_path.endswith('.csv'):
    print(f"{dataset_path} already in csv; no need for conversion")
    darshan_dataset_df = pd.read_csv(dataset_path)
elif dataset_path.endswith('.darshan'):
    print(f"{dataset_path} is a raw darshan log; converting to csv")

    dataset_path = Path(dataset_path)

    # Temporary output file: <ORIGINAL_FILENAME.darshan>.txt
    output_file = dataset_path.with_suffix(dataset_path.suffix + ".txt")

    with open(output_file, "w") as f:
        subprocess.run(
            ["darshan-parser", str(dataset_path)],
            stdout=f,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )

    print(f"Converted log written to: {output_file}; now converting to CSV")
    darshan_dataset_df = read_darshan_text_blocks(output_file)

elif dataset_path.endswith('.txt'):
    print(f"{dataset_path} is a text file; converting to csv")
    darshan_dataset_df = read_darshan_text_blocks(dataset_path)
else:
    print(f"{dataset_path} file format is unsupported; terminating the job!!")
    exit(1)

refined_amrex_dfs = extract_important_counters([(dataset_path, darshan_dataset_df)])
refined_dataset = refined_amrex_dfs[0][1]
refined_dataset = refined_dataset[~(refined_dataset['module'].str.contains('HEATMAP'))]
posix_counters = refined_dataset[(refined_dataset['counter'].str.contains('POSIX'))]


tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=2048,
    # temperature=0.01,
    return_full_text=False   # 🔥 This is the fix
)


llm = HuggingFacePipeline(pipeline=pipe)


# ===============================
# 1️⃣ Create base + timestamped dir
# ===============================

# log_dir = os.path.abspath("../llm_logs")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

session_dir = os.path.join(log_dir, timestamp)
os.makedirs(session_dir, exist_ok=True)

# ===============================
# 2️⃣ Save CSV snapshot
# ===============================

csv_path = os.path.join(session_dir, f"darshan_input_{timestamp}.csv")
darshan_dataset_df.to_csv(csv_path, index=False)

# ===============================
# 3️⃣ Prepare prompts
# ===============================

import os
from datetime import datetime

# ===============================
# 1️⃣ Create prompts list
# ===============================



col = posix_counters["filename"].astype(str)

# Find common prefix
prefix = os.path.commonprefix(list(col))

# Remove prefix
posix_counters["filename"] = col.str[len(prefix):]

group_cols = ['rank', 'filename']

# 1️⃣ Aggregate READ
read_df = (
    posix_counters[
        posix_counters['counter'] == 'POSIX_BYTES_READ'
    ]
    .groupby(group_cols, as_index=False)['value']
    .sum()
    .rename(columns={'value': 'POSIX_BYTES_READ'})
)

# 2️⃣ Aggregate WRITE
write_df = (
    posix_counters[
        posix_counters['counter'] == 'POSIX_BYTES_WRITTEN'
    ]
    .groupby(group_cols, as_index=False)['value']
    .sum()
    .rename(columns={'value': 'POSIX_BYTES_WRITTEN'})
)

# 3️⃣ Outer join to keep all groups
aggregate_bytes_ioed = (
    read_df
    .merge(write_df, on=group_cols, how='outer')
    .fillna(0)
)

write_num = aggregate_bytes_ioed["POSIX_BYTES_WRITTEN"]
read_num = aggregate_bytes_ioed["POSIX_BYTES_READ"]
den = aggregate_bytes_ioed["POSIX_BYTES_WRITTEN"] + aggregate_bytes_ioed["POSIX_BYTES_READ"]

aggregate_bytes_ioed["WRITE_FRAC"] = (
    write_num.div(den.where(den != 0))
    .fillna(0)
)

aggregate_bytes_ioed["READ_FRAC"] = (
    read_num.div(den.where(den != 0))
    .fillna(0)
)

fragmented_size_df = posix_counters.copy()

columns_to_select = ['POSIX_SEQ_WRITES', 'POSIX_WRITES', 'POSIX_SEQ_READS', 'POSIX_READS']

fragmented_size_df = fragmented_size_df[(fragmented_size_df['counter'].isin(columns_to_select))]


group_cols = ['filename']

required_cols = [
    "POSIX_SEQ_WRITES",
    "POSIX_WRITES",
    "POSIX_SEQ_READS",
    "POSIX_READS"
]

fragmented_size_df = (
    fragmented_size_df
    .loc[fragmented_size_df["counter"].isin(required_cols)]
    .groupby(group_cols + ["counter"])["value"]
    .sum()
    .unstack()
    .reindex(columns=required_cols, fill_value=0)   # 👈 force all 4 columns
    .reset_index()
)

num = fragmented_size_df["POSIX_SEQ_WRITES"]
den = fragmented_size_df["POSIX_WRITES"]

fragmented_size_df["WRITE_SEQ_FRAC"] = (
    num.div(den.where(den != 0))
    .fillna(0)
)

num = fragmented_size_df["POSIX_SEQ_READS"]
den = fragmented_size_df["POSIX_READS"]

fragmented_size_df["READ_SEQ_FRAC"] = (
    num.div(den.where(den != 0))
    .fillna(0)
)


short_model_name = model_id.split("/")[-1]
log_path = os.path.join(session_dir, f"llm_conversation_{short_model_name}_{timestamp}.log")
performance_path = os.path.join(session_dir, f"llm_conversation_performance_{short_model_name}_{timestamp}.log")


with open(log_path, "w", encoding="utf-8") as f:
    f.write("=== LLM SESSION LOG ===\n")
    f.write(f"Session Directory: {session_dir}\n")
    f.write(f"Session Timestamp: {timestamp}\n")
    f.write(f"Model Used: {short_model_name}\n")
    f.write(f"Input Dataset File: {dataset_path}\n")
    f.write(f"CSV Snapshot: {csv_path}\n\n")

with open(performance_path, "w", encoding="utf-8") as f:
    f.write("=== LLM SESSION LOG ===\n")
    f.write(f"Session Directory: {session_dir}\n")
    f.write(f"Session Timestamp: {timestamp}\n")
    f.write(f"Model Used: {short_model_name}\n")
    f.write(f"Input Dataset File: {dataset_path}\n")
    f.write(f"CSV Snapshot: {csv_path}\n\n")



total_response_keys = []
past_history = {
        "shared": 0,
        "independent": 0,
        "reads": 0,
        "writes": 0,
        "read_write": 0,
        "huge": 0,
        "small": 0,
        "sequential_write": 0,
        "random_write": 0,
        "sequential_read": 0,
        "random_read": 0
    }

performance_results_per_range = {}

for i in range(0, len(aggregate_bytes_ioed), 5):
    ''' BEGIN prompt for checking read/write, shared/independent and
        huge/small
    '''
    start_idx = i 
    end_idx = min(i + 5, len(aggregate_bytes_ioed))
    prompts = []
    contexts = []
    performance_results = {}
    performance_results_per_range[(start_idx, end_idx)] = {}

    context_1 = f"""
    You are an expert in parallel I/O analysis.

    Definitions:
    - *_FRAC: fraction; between 0.0 and 1.0
    - Shared (Collective) access: files where rank == -1
    - Independent access: files where rank != -1
    - Read files: if READ_FRAC > 0.7
    - Write files: if WRITE_FRAC > 0.7
    - Read/Write files: if WRITE_FRAC >= 0.3 and WRITE_FRAC <= 0.7
    - Huge I/O: > The total read and write >= 1GB
    - Small I/O files: <= The total read and write < 1GB

    Darshan counter definitions:\n
    'POSIX_BYTES_*': {DARSHAN_MODULES['POSIX']['column_description']['POSIX_BYTES_*']}
    'filename': {DARSHAN_MODULES['POSIX']['column_description']['file name']}
    'module': {DARSHAN_MODULES['POSIX']['column_description']['module']}
    'rank': {DARSHAN_MODULES['POSIX']['column_description']['rank']}\n
    """
    output_format = """
    {
        "shared": int,
        "independent": int,
        "reads": int,
        "writes": int,
        "read_write": int,
        "huge": int,
        "small": int
    }
    """
    prompt_1 = (
        "Given these Darshan counters, answer the questions:\n"
        f"{aggregate_bytes_ioed.iloc[start_idx:end_idx
        ].to_string()}\n\n"
        "QUESTION\n"
        "Q1: How many files receive shared vs independent access?\n"
        "Q2: How many files receieve only read, how many do only write, and how many do both read and write?\n"
        "Q3: How many files do receive a huge amount of I/O and how many do small?\n\n"
        "OUTPUT FORMAT (STRICT; DON'T GENERATE EXTRA OUTPUT)\n"
        f"""Return output strictly in JSON with this schema (JUST ONE ANSWER):\n
        {output_format}
        """
        """
        Follow the requested output schema strictly. DON'T ADD QUESTIONS YOURSELF!! DON'T MAKE ASSUMPTIONS
        DON'T GIVE ME THE CODE; do the compute yourself
        """
    )

    prompts.append(prompt_1)
    contexts.append(context_1)


    # We'll generate prompt_2 dynamically after first response
    responses = []

    # ===============================
    # 2️⃣ Run first prompt
    # ===============================

    response_1 = llm.invoke([
        SystemMessage(content=context_1),
        HumanMessage(content=prompt_1)
    ])
    responses.append(response_1)


    shared_independent_performance = report_accuracy_shared_independent(
                                    response_1, 
                                    posix_counters, 
                                    aggregate_bytes_ioed.iloc[start_idx:end_idx
                                    ]['filename'].unique(), 
                                    module='POSIX')


    read_write_performance = report_accuracy_read_write(
                                    response_1, 
                                    posix_counters, 
                                    aggregate_bytes_ioed.iloc[start_idx:end_idx
                                    ]['filename'].unique(), 
                                    module='POSIX')

    huge_small_performance = report_accuracy_huge_small(response_1, posix_counters,
                                    aggregate_bytes_ioed.iloc[start_idx:end_idx
                                    ]['filename'].unique(), 
                                    module='POSIX')

    performance_results['Shared or Independent Access'] = shared_independent_performance
    performance_results['READ or WRITE'] = read_write_performance
    performance_results['Huge or Small'] = huge_small_performance

    ''' END prompt for checking read/write, shared/independent and
        huge/small
    '''

    
    fragmented_size_df_start_end = fragmented_size_df[
        fragmented_size_df['filename'].isin(aggregate_bytes_ioed.iloc[start_idx:end_idx
                                    ]['filename'].unique())
        ]
    fragmented_size_df_start_end = fragmented_size_df_start_end.fillna(0)

    context_2 = f"""
    You are an expert in parallel I/O analysis.

    Definitions:
    - *_FRAC: fraction; between 0.0 and 1.0
    - Sequential write: if the WRITE_SEQ_FRAC >= 0.9, random if less than or equal to 0.1, 
        otherwise neither sequential nor random
        if the POSIX_WRITES is zero, it is neither sequential nor random
    - sequential read: if the READ_SEQ_FRAC >= 0.9, random if less than or equal to 0.1, 
        otherwise neither sequential nor random
        if the POSIX_READS is zero, it is neither sequential nor random.
    - Large I/O size: The I/O size >= 1 MB
    - Small I/O size: The I/O size < 1 MB

    Darshan counter definitions:\n
    'POSIX_*': {DARSHAN_MODULES['POSIX']['column_description']['POSIX_*']}
    'POSIX_SEQ_*': {DARSHAN_MODULES['POSIX']['column_description']['POSIX_SEQ_*']}
    'filename': {DARSHAN_MODULES['POSIX']['column_description']['file name']}
    'module': {DARSHAN_MODULES['POSIX']['column_description']['module']}
    'rank': {DARSHAN_MODULES['POSIX']['column_description']['rank']}\n
    Follow the requested output schema strictly. DON'T ADD QUESTIONS YOURSELF!! DON'T MAKE ASSUMPTIONS!!
    DON'T GIVE ME THE CODE; do the compute yourself
    """
    output_format = """
    {
        "sequential_write": int,
        "random_write": int,
        "sequential_read": int,
        "random_read": int
    }
    """
    prompt_2 = (
        "Given these Darshan counters, answer the questions:\n"
        f"{fragmented_size_df_start_end.to_string()}\n\n"
        "QUESTION\n"
        "Q1: How many files are sequential, and how many are random? (ASSUME any counter not given is zero\n"
        "OUTPUT FORMAT (STRICT; DON'T GENERATE Explanations)\n"
        f"""Return output strictly in JSON with this schema (JUST ONE ANSWER):\n
        {output_format}
        """
    )

    prompts.append(prompt_2)
    contexts.append(context_2)

    response_2 = llm.invoke([
        SystemMessage(content=context_2),
        HumanMessage(content=prompt_2)
    ])
    responses.append(response_2)

    # report_accuracy_sequential_random(response_2, darshan_csv, file_list)

    sequential_random_performance = report_accuracy_sequential_random(
                                    response_2, 
                                    posix_counters, 
                                    fragmented_size_df_start_end["filename"].unique(), 
                                    module='POSIX')

    performance_results['Sequential or Random'] = sequential_random_performance

    try:
        response_1_json = extract_last_json(response_1)
    except ValueError as e:
        response_1_json = {
            "shared": 0,
            "independent": 0,
            "reads": 0,
            "writes": 0,
            "read_write": 0,
            "huge": 0,
            "small": 0,
        }
    try:
        response_2_json = extract_last_json(response_2)
    except ValueError as e:
        response_2_json = {
            "sequential_write": 0,
            "random_write": 0,
            "sequential_read": 0,
            "random_read": 0
        }

    # response_dicts = [response_1_json, response_2_json]

    # json_response_merged = {}
    # for d in response_dicts:
    #     json_response_merged.update(d)



    context_summary = f"""
    You are an expert in parallel I/O analysis. The I/O patterns provide a json string each
    listing counters; your task is to concatenate the two json dicts, and to add the 
    `past_history` dict (Whatever seen before) to the resulting json key-val-wise (The history format is IDENTICAL TO THE OUTPUT FORMAT),
    so it becomes:

    result = CONCAT(pattern 1, pattern 2) + HISTORY

    Follow the requested output schema strictly. DON'T ADD QUESTIONS YOURSELF!! DON'T MAKE ASSUMPTIONS
    DON'T GIVE ME THE CODE; do the compute yourself
    """

    output_format = """
    {
        "shared": int,
        "independent": int,
        "reads": int,
        "writes": int,
        "read_write": int,
        "huge": int,
        "small": int,
        "sequential_write": int,
        "random_write": int,
        "sequential_read": int,
        "random_read": int
    }
    """
    ## Summarization
    prompt_summary = (
        "Compute the result given the following:\n"
        "PAST HISTORY: \n"
        f"{past_history}\n\n"
        "Pattern I:\n"
        f"{response_1_json}\n\n"
        "Pattern II:\n"
        f"{response_2_json}\n\n"
        "OUTPUT FORMAT (STRICT; DON'T GENERATE EXTRA OUTPUT)\n"
        f"""Return output strictly in JSON with this schema (JUST ONE ANSWER):\n
        {output_format}"""
    )

    prompts.append(prompt_summary)
    contexts.append(context_summary)

    response_summary = llm.invoke(prompt_summary)
    responses.append(response_summary)

    summarization_performance = report_accuracy_summarization(
                                    response_summary, 
                                    posix_counters,
                                    past_history, 
                                    response_1,
                                    response_2,
                                    aggregate_bytes_ioed.iloc[start_idx:end_idx
                                    ]['filename'].unique(), 
                                    module='POSIX')
    performance_results['summarization'] = summarization_performance

    for key, val in summarization_performance.items():
        new_val = summarization_performance[key]['output']
        past_history[key] += new_val


    performance_results_per_range[(start_idx, end_idx)] = performance_results


    # ===============================
    # 3️⃣ Persist Everything
    # ===============================

    with open(log_path, "a", encoding="utf-8") as f:

        for j, (context, prompt, response) in enumerate(\
            zip(contexts, prompts, responses), start=1):

            f.write(f"============BEGIN FILE RANGE ({i}, {min((i + 5), len(aggregate_bytes_ioed))} ===========\n\n")

            f.write(f"----- CONTEXT {j} -----\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(context + "\n\n")

            f.write(f"----- PROMPT {j} -----\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(prompt + "\n\n")

            f.write(f"----- RESPONSE {j} -----\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(response + "\n")

            f.write(f"============ END FILE RANGE ({i}, {min((i + 5), len(aggregate_bytes_ioed))} ===========\n\n")


    with open(performance_path, "a", encoding="utf-8") as f:
        import json

        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        f.write(f"============BEGIN FILE RANGE ({i}, {min((i + 5), len(aggregate_bytes_ioed))}))===========\n\n")
        for result_key, result_val in performance_results.items():
            print(f">>>>>>>>>  BEGIN {result_key} <<<<<<<<<", file=f)
            print(
                json.dumps(
                    result_val,
                    indent=4,
                    default=convert_numpy
                ),
                file=f
            )
            print(file=f)
            print(file=f)
            print_accuracy_stat(result_val, log_file=f)
            print(f">>>>>>>>>  END {result_key} <<<<<<<<<", file=f)
        f.write(f"============END FILE RANGE ({i}, {min((i + 5), len(aggregate_bytes_ioed))}))===========\n\n")



total_accuracy_scores = {}
for _range, scores_dict in performance_results_per_range.items():
    print(f"Range = {_range}")
    print(f"scores_dict = {scores_dict}")
    for prompt_method, results in scores_dict.items():

        for key, metrics in results.items():
            if key not in total_accuracy_scores:
                total_accuracy_scores[key] = {
                    "output": 0,
                    "expected": 0
                }

            total_accuracy_scores[key]["output"] += int(metrics["output"])
            total_accuracy_scores[key]["expected"] += int(metrics["expected"])


# -----------------------------
# 2️⃣ Compute accuracy
# -----------------------------
summary = {}

for method, vals in total_accuracy_scores.items():
    output = vals["output"]
    expected = vals["expected"]

    accuracy = output / expected if expected != 0 else "Undef"

    summary[method] = {
        "total_output": output,
        "total_expected": expected,
        "accuracy": accuracy
    }

# -----------------------------
# 3️⃣ Save to JSON file
# -----------------------------
accuracy_summary_json = os.path.join(session_dir, f"accuracy_summary_{timestamp}.json")
with open(accuracy_summary_json, "w") as f:
    json.dump(summary, f, indent=4)

print("Saved summary to accuracy_summary.json")



print("All prompts and responses saved.")


# ===============================
# 5️⃣ Print results
# ===============================

# print(pattern_response)
# print(summarized_pattern_response)

print("\nSession saved to:")
print(session_dir)
