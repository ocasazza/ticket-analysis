#!/usr/bin/env python
"""
Create smaller sample CSV files for the GitHub Pages deployment.
The original files are likely too large for GitHub Pages to handle efficiently.
"""

import os
import csv
import random

# Source and destination directories
source_dir = "data/fresh_service_tickets"
dest_dir = "jupyter-lite/content/data/fresh_service_tickets"

# Ensure destination directory exists
os.makedirs(dest_dir, exist_ok=True)

# Parameters for sample creation
SAMPLE_SIZE = 100  # Number of rows to include in the sample
RANDOM_SEED = 42   # For reproducibility

# Create samples for each CSV file
for filename in os.listdir(source_dir):
    if filename.endswith(".csv"):
        # Path to source file
        src_file = os.path.join(source_dir, filename)
        # Path to destination file (keep the same name)
        dst_file = os.path.join(dest_dir, filename)
        
        print(f"Creating sample for {filename}...")
        
        # Find a working encoding and read file info
        encoding_found = False
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                # Read header and count rows
                with open(src_file, 'r', encoding=encoding) as f:
                    reader = csv.reader(f)
                    header = next(reader)  # Get the header row
                    
                    # Count rows (up to 1000 for performance)
                    row_count = 0
                    for _ in range(1000):
                        try:
                            next(reader)
                            row_count += 1
                        except StopIteration:
                            break
                
                # If we got here without errors, we found a working encoding
                encoding_found = True
                working_encoding = encoding
                break
            
            except UnicodeDecodeError:
                print(f"  Encoding {encoding} failed, trying another...")
                continue
        
        if not encoding_found:
            print(f"  Could not read {filename} with any of the attempted encodings")
            continue  # Skip to the next file
        
        # Decide sampling strategy based on file size
        if row_count <= SAMPLE_SIZE:
            # If file is already small, just copy it
            print(f"  File {filename} is already small ({row_count} rows). Copying directly.")
            with open(src_file, 'r', encoding=working_encoding) as src, open(dst_file, 'w', encoding='utf-8', newline='') as dst:
                dst.write(src.read())
        else:
            # For larger files, take a random sample
            print(f"  File {filename} has at least {row_count} rows. Creating a {SAMPLE_SIZE}-row sample.")
            
            # Use random sampling for larger files
            random.seed(RANDOM_SEED)
            
            # Read all rows
            with open(src_file, 'r', encoding=working_encoding) as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = list(reader)
            
            # Randomly sample rows
            if len(rows) > SAMPLE_SIZE:
                sampled_rows = random.sample(rows, SAMPLE_SIZE)
            else:
                sampled_rows = rows
            
            # Write the sample file
            with open(dst_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(sampled_rows)
            
            print(f"  Created sample with {len(sampled_rows) + 1} rows (including header).")

print("Done! Sample CSV files created in:", dest_dir)
