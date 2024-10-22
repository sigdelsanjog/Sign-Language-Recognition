# log_progress.py

import os
import pandas as pd

def calc_landmark_extraction_time(processed_images, current_elapsed_time, tab_name, progress_excel):
    # Create a DataFrame for the current progress
    progress_data = pd.DataFrame({
        'Processed Images': [processed_images], 
        'Elapsed Time': [current_elapsed_time]
    })

    # Try to read the existing data from the Excel file
    if os.path.exists(progress_excel):
        # Check if the sheet exists
        with pd.ExcelFile(progress_excel) as xls:
            existing_sheets = xls.sheet_names
            if tab_name in existing_sheets:
                # Read existing data
                existing_data = pd.read_excel(xls, sheet_name=tab_name)
                
                # Calculate time difference based on the last elapsed time
                if not existing_data.empty:
                    last_elapsed_time = existing_data['Elapsed Time'].iloc[-1]  # Last entry elapsed time
                    time_difference = current_elapsed_time - last_elapsed_time
                    progress_data['Time Difference'] = time_difference
                else:
                    progress_data['Time Difference'] = None  # No previous data for first run

                # Append new data to the existing data
                updated_data = pd.concat([existing_data, progress_data], ignore_index=True)
            else:
                # If the sheet does not exist, create a new one
                progress_data['Time Difference'] = None
                updated_data = progress_data
    else:
        # Write to the Excel file if it doesn't exist yet
        updated_data = progress_data

    # Save updated data to the Excel file
    with pd.ExcelWriter(progress_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_data.to_excel(writer, sheet_name=tab_name, index=False)

    print(f"Progress logged for {processed_images} images.")
