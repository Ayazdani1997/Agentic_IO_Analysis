import pandas as pd

import os
import argparse

import sys
import os
from datetime import datetime
from io import StringIO
import json
import numpy as np
import sys


def extract_last_json(response: str):
        start = response.rfind("{")
        end = response.rfind("}")
        
        if start == -1 or end == -1 or end < start:
            raise ValueError("No valid JSON object found in string.")
        
        json_str = response[start:end + 1]
        
        return json.loads(json_str)


def print_accuracy_stat(performance, log_file=sys.stdout):
    for category, values in performance.items():
    
        expected = values["expected"]
        output = values["output"]
        
        if expected != 0:
            if output > expected:
                accuracy = (output - expected) / expected
            else:
                accuracy = output / expected
        else:
            accuracy = 0 if output != 0 else 1
        
        print(f"\nCategory: {category}", file=log_file)
        print(f"Expected: {expected}", file=log_file)
        print(f"Output: {output}", file=log_file)
        print(f"Accuracy: {accuracy:.2%}", file=log_file)