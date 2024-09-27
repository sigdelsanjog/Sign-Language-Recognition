import os
import pandas as pd

# Function to count files inside each sub-folder (like A, B, C, D, etc.)
def count_files_in_subfolders(directory):
    file_counts = {}
    
    for root, dirs, files in os.walk(directory):
        subfolder = os.path.basename(root)
        if subfolder != os.path.basename(directory):  # Ignore the main directory itself
            file_counts[subfolder] = len(files)
    
    return file_counts

# Function to create a DataFrame for file counts in each chunk folder
def count_files_in_chunks(main_directory):
    chunk_data = {}
    
    # Loop through each chunk directory (chunk1, chunk2, apple, etc.)
    for chunk_folder in os.listdir(main_directory):
        chunk_path = os.path.join(main_directory, chunk_folder)
        if os.path.isdir(chunk_path):
            # Count the number of files in the subfolders (A, B, C, 1, 2, etc.)
            file_counts = count_files_in_subfolders(chunk_path)
            chunk_data[chunk_folder] = file_counts

    # Create a DataFrame from the collected file counts
    df = pd.DataFrame(chunk_data).fillna(0).astype(int)  # Fill missing values with 0 and cast to int
    return df

# Function to count files in a specific directory (for chunk directory)
def count_files_in_directory(directory):
    file_count = {}
    
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            file_count[folder] = len(os.listdir(folder_path))  # Count files directly

    return file_count

# Main execution
directory1 = "dataset_chunks"  # Path to the first directory
chunk_directory = "dataset_5G"   # Path to the chunk directory

# Count files in both directories
file_count= count_files_in_chunks(directory1)

# Count files in the chunk directory
chunk_file_counts = count_files_in_directory(chunk_directory)
chunk_df = pd.DataFrame.from_dict(chunk_file_counts, orient='index', columns=['File Count']).reset_index()
chunk_df.rename(columns={'index': 'Folder'}, inplace=True)

# Create a Pandas Excel writer using openpyxl
output_excel = 'file_counts_with_chunks.xlsx'
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    file_count.to_excel(writer, sheet_name='chunk_count')
    chunk_df.to_excel(writer, sheet_name='5GB', index=False)

print(f"\nFile counts saved to {output_excel} with two sheets: chunk_count and 5GB.")
