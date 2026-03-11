import pandas as pd

import os
import argparse

import sys
import os
from datetime import datetime
from io import StringIO
import json
import numpy as np
from .utils import *

import json


SCALE_THRESHOLD = 1 * 1024 * 1024 * 1024

def report_accuracy_shared_independent(response, darshan_csv, file_list, module='POSIX'):
    print('======================= BEGIN Testing SHARED VS INDEPENDENT ACCESS =============================')
    module_counters = darshan_csv
    module_counters = module_counters[module_counters['filename'].isin(file_list)]
    group_cols = ['rank', 'filename']

    # 1️⃣ Aggregate READ
    read_df = (
        module_counters[
            module_counters['counter'] == f"{module}_BYTES_READ"
        ]
        .groupby(group_cols, as_index=False)['value']
        .sum()
        .rename(columns={'value': f"{module}_BYTES_READ"})
    )

    # 2️⃣ Aggregate WRITE
    write_df = (
        module_counters[
            module_counters['counter'] == f"{module}_BYTES_WRITTEN"
        ]
        .groupby(group_cols, as_index=False)['value']
        .sum()
        .rename(columns={'value': f"{module}_BYTES_WRITTEN"})
    )

    # 3️⃣ Outer join to keep all groups
    aggregate_bytes_ioed = (
        read_df
        .merge(write_df, on=group_cols, how='outer')
        .fillna(0)
    )

    shared_files = aggregate_bytes_ioed[aggregate_bytes_ioed['rank'] == -1]
    independent_files = aggregate_bytes_ioed[aggregate_bytes_ioed['rank'] != -1]

    expected_independent_files = independent_files['filename'].nunique()
    expected_shared_files = shared_files['filename'].nunique()
    try:
        llm_output = extract_last_json(response)

        output_shared = llm_output['shared']
        output_independent = llm_output['independent']

        print(f"output_shared = {output_shared}, output_independent = {output_independent}")
    except ValueError as e:
        print("ValueError")
        print(e)
        output_shared = 0
        output_independent = 0
    performance_result = {
                            'independent': 
                                    {
                                        'expected': expected_independent_files, 
                                        'output': output_independent
                                    }, 
                            'shared': 
                                    {
                                        'expected': expected_shared_files, 
                                        'output': output_shared
                                    }
                         }
    print(performance_result)
    print_accuracy_stat(performance_result)
    print('======================= END Testing SHARED VS INDEPENDENT ACCESS =============================')
    return performance_result



def report_accuracy_read_write(response, darshan_csv, file_list, module='POSIX'):
    print('======================= BEGIN Testing READ WRITE ACCESS =============================')
    module_counters = darshan_csv
    module_counters = module_counters[module_counters['filename'].isin(file_list)]
    group_cols = ['filename']

    # 1️⃣ Aggregate READ
    read_df = (
        module_counters[
            module_counters['counter'] == f"{module}_BYTES_READ"
        ]
        .groupby(group_cols, as_index=False)['value']
        .sum()
        .rename(columns={'value': f"{module}_BYTES_READ"})
    )

    # 2️⃣ Aggregate WRITE
    write_df = (
        module_counters[
            module_counters['counter'] == f"{module}_BYTES_WRITTEN"
        ]
        .groupby(group_cols, as_index=False)['value']
        .sum()
        .rename(columns={'value': f"{module}_BYTES_WRITTEN"})
    )

    # 3️⃣ Outer join to keep all groups
    aggregate_bytes_ioed = (
        read_df
        .merge(write_df, on=group_cols, how='outer')
        .fillna(0)
    )

    fragmented_bytes_read_write = aggregate_bytes_ioed.copy()

    write_num = fragmented_bytes_read_write[f"{module}_BYTES_WRITTEN"]
    read_num = fragmented_bytes_read_write[f"{module}_BYTES_READ"]
    den = fragmented_bytes_read_write[f"{module}_BYTES_WRITTEN"] + fragmented_bytes_read_write[f"{module}_BYTES_READ"]

    fragmented_bytes_read_write["WRITE_FRAC"] = (
        write_num.div(den.where(den != 0))
        .fillna(0)
    )

    fragmented_bytes_read_write["READ_FRAC"] = (
        read_num.div(den.where(den != 0))
        .fillna(0)
    )

    fragmented_bytes_read_write["IS_READ_FILE"] = fragmented_bytes_read_write["READ_FRAC"] > 0.7

    fragmented_bytes_read_write["IS_WRITE_FILE"] = fragmented_bytes_read_write["WRITE_FRAC"] > 0.7

    fragmented_bytes_read_write["IS_READ_WRITE_FILE"] = (
        (fragmented_bytes_read_write["WRITE_FRAC"] >= 0.3) &
        (fragmented_bytes_read_write["WRITE_FRAC"] <= 0.7)
    )

    try: 
        llm_output = extract_last_json(response)

        output_read_write = llm_output['read_write']
        output_write = llm_output['writes']
        output_read = llm_output['reads']
    except ValueError as e:
        output_read_write = 0
        output_write = 0
        output_read = 0

    expected_read_write = fragmented_bytes_read_write["IS_READ_WRITE_FILE"].sum()
    expected_read = fragmented_bytes_read_write["IS_READ_FILE"].sum()
    expected_write = fragmented_bytes_read_write["IS_WRITE_FILE"].sum()


    performance_result = {
                            'read_write': 
                                    {
                                        'expected': expected_read_write, 
                                        'output': output_read_write
                                    }, 
                            'writes': 
                                    {
                                        'expected': expected_write, 
                                        'output': output_write
                                    }, 
                            'reads': 
                                    {
                                        'expected': expected_read, 
                                        'output': output_read
                                    }, 
                         }

    print_accuracy_stat(performance_result)

    print('======================= END Testing READ WRITE ACCESS =============================')


    return performance_result


def report_accuracy_huge_small(response, darshan_csv, file_list, module='POSIX'):
    print('======================= BEGIN Testing SCALE ACCESS =============================')
    threshold = SCALE_THRESHOLD
    module_counters = darshan_csv
    module_counters = module_counters[module_counters['filename'].isin(file_list)]
    group_cols = ['filename']

    # 1️⃣ Aggregate READ
    read_df = (
        module_counters[
            module_counters['counter'] == f"{module}_BYTES_READ"
        ]
        .groupby(group_cols, as_index=False)['value']
        .sum()
        .rename(columns={'value': f"{module}_BYTES_READ"})
    )

    # 2️⃣ Aggregate WRITE
    write_df = (
        module_counters[
            module_counters['counter'] == f"{module}_BYTES_WRITTEN"
        ]
        .groupby(group_cols, as_index=False)['value']
        .sum()
        .rename(columns={'value': f"{module}_BYTES_WRITTEN"})
    )

    # 3️⃣ Outer join to keep all groups
    aggregate_bytes_ioed = (
        read_df
        .merge(write_df, on=group_cols, how='outer')
        .fillna(0)
    )

    fragmented_bytes_read_write = aggregate_bytes_ioed.copy()

    write_num = fragmented_bytes_read_write[f"{module}_BYTES_WRITTEN"]
    read_num = fragmented_bytes_read_write[f"{module}_BYTES_READ"]
    fragmented_bytes_read_write[f"{module}_BYTES"] = fragmented_bytes_read_write[f"{module}_BYTES_WRITTEN"] + fragmented_bytes_read_write["POSIX_BYTES_READ"]


    fragmented_bytes_read_write["IS_HUGE"] = fragmented_bytes_read_write[f"{module}_BYTES"] >= threshold

    fragmented_bytes_read_write["IS_SMALL"] = fragmented_bytes_read_write[f"{module}_BYTES"] < threshold


    try: 
        llm_output = extract_last_json(response)
        output_small = llm_output['small']
        output_huge = llm_output['huge']
    except ValueError as e:
        output_small = 0
        output_huge = 0

    expected_small = fragmented_bytes_read_write["IS_SMALL"].sum()
    expected_huge = fragmented_bytes_read_write["IS_HUGE"].sum()


    performance_result = {
                            'small': 
                                    {
                                        'expected': expected_small, 
                                        'output': output_small
                                    }, 
                            'huge': 
                                    {
                                        'expected': expected_huge, 
                                        'output': output_huge
                                    }, 
                         }

    print_accuracy_stat(performance_result)

    print('======================= END Testing SCALE ACCESS =============================')


    return performance_result





# def report_accuracy_io_size_per_file(response, darshan_csv, file_list):
#     pass

def report_accuracy_sequential_random(response, darshan_csv, file_list, module='POSIX'):

    print('======================= BEGIN Testing SEQ RANDOM ACCESS =============================')

    fragmented_size_df = darshan_csv[darshan_csv["filename"].isin(file_list)]

    columns_to_select = [f"{module}_SEQ_WRITES", f"{module}_WRITES", f"{module}_SEQ_READS", f"{module}_READS"]

    fragmented_size_df_seq_counters = fragmented_size_df[(fragmented_size_df['counter'].isin(columns_to_select))]


    group_cols = ['filename']

    required_cols = [
        f"{module}_SEQ_WRITES",
        f"{module}_WRITES",
        f"{module}_SEQ_READS",
        f"{module}_READS"
    ]

    fragmented_size_df_seq_counters = (
        fragmented_size_df_seq_counters
        .loc[fragmented_size_df_seq_counters["counter"].isin(required_cols)]
        .groupby(group_cols + ["counter"])["value"]
        .sum()
        .unstack()
        .reindex(columns=required_cols, fill_value=0)   # 👈 force all 4 columns
        .reset_index()
    )

    num = fragmented_size_df_seq_counters[f"{module}_SEQ_WRITES"]
    den = fragmented_size_df_seq_counters[f"{module}_WRITES"]

    fragmented_size_df_seq_counters["WRITE_SEQ_FRAC"] = (
        num.div(den.where(den != 0))
        .fillna(0)
    )

    num = fragmented_size_df_seq_counters[f"{module}_SEQ_READS"]
    den = fragmented_size_df_seq_counters[f"{module}_READS"]

    fragmented_size_df_seq_counters["READ_SEQ_FRAC"] = (
        num.div(den.where(den != 0))
        .fillna(0)
    )

    # print(fragmented_size_df_seq_counters["READ_SEQ_FRAC"].dtype)
    fragmented_size_df_seq_counters = fragmented_size_df_seq_counters.fillna(0)


    fragmented_size_df_seq_counters["IS_SEQUENTIAL_READ_FILE"] = (fragmented_size_df_seq_counters["READ_SEQ_FRAC"] >= 0.9) \
                                                                    & (fragmented_size_df_seq_counters[f"{module}_READS"] != 0)
    fragmented_size_df_seq_counters["IS_SEQUENTIAL_WRITE_FILE"] = (fragmented_size_df_seq_counters["WRITE_SEQ_FRAC"] >= 0.9) \
                                                                & (fragmented_size_df_seq_counters[f"{module}_WRITES"] != 0)
    fragmented_size_df_seq_counters["IS_RANDOM_READ_FILE"] = (fragmented_size_df_seq_counters["READ_SEQ_FRAC"] <= 0.1) \
                                                            & (fragmented_size_df_seq_counters[f"{module}_READS"] != 0)
    fragmented_size_df_seq_counters["IS_RANDOM_WRITE_FILE"] = (fragmented_size_df_seq_counters["WRITE_SEQ_FRAC"] <= 0.1) \
                                                                & (fragmented_size_df_seq_counters[f"{module}_WRITES"] != 0)

    print(fragmented_size_df_seq_counters.to_string())

    expected_sequential_write = fragmented_size_df_seq_counters["IS_SEQUENTIAL_WRITE_FILE"].sum()
    expected_random_write = fragmented_size_df_seq_counters["IS_RANDOM_WRITE_FILE"].sum()
    expected_sequential_read = fragmented_size_df_seq_counters["IS_SEQUENTIAL_READ_FILE"].sum()
    expected_random_read = fragmented_size_df_seq_counters["IS_RANDOM_READ_FILE"].sum()



    try: 
        llm_output = extract_last_json(response)

        output_sequential_write = llm_output['sequential_write']
        output_random_write = llm_output['random_write']
        output_sequential_read = llm_output['sequential_read']
        output_random_read = llm_output['random_read']
    except ValueError as e:
        output_sequential_write = 0
        output_random_write = 0
        output_sequential_read = 0
        output_random_read = 0

    performance_result = {
                            'sequential_read': 
                                    {
                                        'expected': expected_sequential_read, 
                                        'output': output_sequential_read
                                    }, 
                            'sequential_write': 
                                    {
                                        'expected': expected_sequential_write, 
                                        'output': output_sequential_write
                                    }, 
                            'random_read': 
                                    {
                                        'expected': expected_random_read, 
                                        'output': output_random_read
                                    }, 
                            'random_write': 
                                    {
                                        'expected': expected_random_write, 
                                        'output': output_random_write
                                    }, 
                         }

    print_accuracy_stat(performance_result)

    print('======================= END Testing SEQ RANDOM ACCESS =============================')

    return performance_result
    

def report_accuracy_summarization(response, darshan_csv, past_history, pattern_1, pattern_2, file_list, module='POSIX'):
    print('======================= BEGIN Testing SUMMARIZATION =============================')
    pattern_1_checkers = {
                'read write': report_accuracy_read_write, 
                'small huge': report_accuracy_huge_small,
                'shared independent': report_accuracy_shared_independent
                }
    
    pattern_2_checkers = {
        'sequential random': report_accuracy_sequential_random
    }
    checker_results = {}
    for name, checker in pattern_1_checkers.items():
        perf_result = checker(pattern_1, darshan_csv, file_list, module)
        for key, val in perf_result.items():
            checker_results[key] = {}
            checker_results[key]['expected'] = val['expected']

    for name, checker in pattern_2_checkers.items():
        perf_result = checker(pattern_2, darshan_csv, file_list, module)
        for key, val in perf_result.items():
            checker_results[key] = {}
            checker_results[key]['expected'] = val['expected']

    for key, val in past_history.items():
        checker_results[key]['expected'] += val


    try: 
        llm_output = extract_last_json(response)
        print(f">>>>>>>>>>> BEGIN LLM output:")
        print(llm_output)
        print(f">>>>>>>>>>> END LLM output:")

    except ValueError as e:
        llm_output = ""
    for key, val in checker_results.items():
        print(f"key = {key}")
        if key not in llm_output:
            checker_results[key]['output'] = 0
        else:
            checker_results[key]['output'] = llm_output[key]

    print_accuracy_stat(checker_results)
    print('======================= END Testing SUMMARIZATION =============================')
    
    return checker_results
    



def report_accuracy_textualization(response, darshan_csv, drishti_csv, file_list):
    pass