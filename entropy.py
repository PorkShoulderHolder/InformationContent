import os
import math
from collections import Counter
from tqdm import tqdm

def calculate_file_entropy(filename):
    """
    Calculate the entropy of a file in bits per byte, with a progress bar.

    Parameters:
    filename (str): The path to the file.

    Returns:
    float: The entropy value.
    """
    file_size = os.path.getsize(filename)
    if file_size == 0:
        return 0.0  # Handle empty file

    byte_counts = Counter()
    total_bytes = 0

    with open(filename, 'rb') as f, tqdm(total=file_size, unit='B', unit_scale=True, desc='Processing') as pbar:
        while True:
            chunk = f.read(65536)  # Read in chunks of 64KB
            if not chunk:
                break
            byte_counts.update(chunk)
            bytes_read = len(chunk)
            total_bytes += bytes_read
            pbar.update(bytes_read)

    entropy = 0.0
    for count in byte_counts.values():
        p_x = count / total_bytes
        entropy -= p_x * math.log2(p_x)
    return entropy

import sys
import os
entropy_per_byte = calculate_file_entropy(sys.argv[1])
print("entropy per byte:", entropy_per_byte) 
file_size_in_bytes = os.path.getsize(sys.argv[1])
total_information_bits = entropy_per_byte * file_size_in_bytes / (8.0 * 1000000000)
print(f"Total information in the file: {total_information_bits} GB")
