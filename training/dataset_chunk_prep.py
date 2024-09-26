import os
import shutil
import pandas as pd
import math

# Function to count files inside each sub-folder (like A, B, C, D, etc.)
def count_files_in_subfolders(directory):
    file_counts = {}
    
    for root, dirs, files in os.walk(directory):
        subfolder = os.path.basename(root)
        if subfolder != os.path.basename(directory):  # Ignore the main directory itself
            file_counts[subfolder] = len(files)
    
    return file_counts

# Function to divide files into 25%, 50%, and 75% chunks
def divide_files_into_chunks(subfolder_path, destination_dir, subfolder_name, file_list):
    total_files = len(file_list)
    
    # Calculate sizes for each chunk
    chunk_25_size = math.ceil(total_files * 0.25)
    chunk_50_size = math.ceil(total_files * 0.50)
    chunk_75_size = math.ceil(total_files * 0.75)
    
    # Create chunk folders
    chunk_25_dir = os.path.join(destination_dir, "chunk_25", subfolder_name)
    chunk_50_dir = os.path.join(destination_dir, "chunk_50", subfolder_name)
    chunk_75_dir = os.path.join(destination_dir, "chunk_75", subfolder_name)
    os.makedirs(chunk_25_dir, exist_ok=True)
    os.makedirs(chunk_50_dir, exist_ok=True)
    os.makedirs(chunk_75_dir, exist_ok=True)
    
    # Copy files to the respective chunk folders
    for i, file_name in enumerate(file_list):
        file_path = os.path.join(subfolder_path, file_name)
        
        # Copy to chunk_25
        if i < chunk_25_size:
            shutil.copy(file_path, os.path.join(chunk_25_dir, file_name))
        
        # Copy to chunk_50
        if i < chunk_50_size:
            shutil.copy(file_path, os.path.join(chunk_50_dir, file_name))
        
        # Copy to chunk_75
        if i < chunk_75_size:
            shutil.copy(file_path, os.path.join(chunk_75_dir, file_name))

# Function to create 25%, 50%, and 75% file chunks for each sub-folder in the main directory
def create_chunks_from_subfolders(main_directory, destination_dir):
    # Loop through each sub-folder
    for subfolder_name in os.listdir(main_directory):
        subfolder_path = os.path.join(main_directory, subfolder_name)
        if os.path.isdir(subfolder_path):
            # Get the list of files
            file_list = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
            # Divide files into 25%, 50%, and 75% chunks
            divide_files_into_chunks(subfolder_path, destination_dir, subfolder_name, file_list)

# Function to create a DataFrame for file counts in each chunk folder
def count_files_in_chunks(destination_dir):
    chunk_data = {}

    # Count files for each chunk (chunk_25, chunk_50, chunk_75)
    for chunk_folder in ["chunk_25", "chunk_50", "chunk_75"]:
        chunk_path = os.path.join(destination_dir, chunk_folder)
        file_counts = count_files_in_subfolders(chunk_path)
        chunk_data[chunk_folder] = file_counts

    # Create a DataFrame from the collected file counts
    df = pd.DataFrame(chunk_data).fillna(0).astype(int)  # Fill missing values with 0 and cast to int
    return df

# Main execution
main_directory = "dataset_5G"  # Path to the main directory (like dataset_5G)
destination_dir = "dataset_chunks"  # Directory where chunk_25, chunk_50, and chunk_75 will be created

# Step 1: Create 25%, 50%, and 75% chunks from subfolders
create_chunks_from_subfolders(main_directory, destination_dir)

# Step 2: Count files in each chunk
file_count_df = count_files_in_chunks(destination_dir)

# Step 3: Save the file counts into an Excel file
output_excel = 'file_counts_with_chunks.xlsx'
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    file_count_df.to_excel(writer, sheet_name='Chunk File Counts')

print(f"\nFile counts for each chunk (25%, 50%, 75%) saved to {output_excel}")
