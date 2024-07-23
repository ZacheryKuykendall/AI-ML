import os
import shutil
from math import ceil

def split_folder(source_folder, destination_folder, files_per_chunk):
    # Get all files from the source folder
    all_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    # Calculate the number of chunks
    num_chunks = ceil(len(all_files) / files_per_chunk)
    
    for i in range(num_chunks):
        # Create a new folder for each chunk
        chunk_folder = os.path.join(destination_folder, f"chunk_{i+1}")
        os.makedirs(chunk_folder, exist_ok=True)
        
        # Get the files for this chunk
        chunk_files = all_files[i*files_per_chunk : (i+1)*files_per_chunk]
        
        # Move files to the chunk folder
        for file in chunk_files:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(chunk_folder, file)
            shutil.move(source_path, destination_path)
        
        print(f"Moved {len(chunk_files)} files to {chunk_folder}")

# Usage
source_folder = "/path/to/your/source/folder"
destination_folder = "/path/to/your/destination/folder"
files_per_chunk = 25000

split_folder(source_folder, destination_folder, files_per_chunk)