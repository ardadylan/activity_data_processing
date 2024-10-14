import pandas as pd
import numpy as np
import glob
import os  # To handle file paths


# Ask the user for the directory containing the CSV files
directory = input("Please enter the directory path containing the CSV files: ")

# Use glob to find all CSV files in the specified directory
file_paths = glob.glob(os.path.join(directory, '*.csv'))  # This combines the directory with the CSV pattern

# Loop through each CSV file
for file_path in file_paths:
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check and print columns to verify the DataFrame structure
        print(f"Processing file: {file_path}")
        print(f"Columns in {file_path}: {df.columns.tolist()}")

        # Convert the timestamp column to datetime if 'time' column exists, 'time' column only exists in files we want to read
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])

            # Extract the date from the timestamp
            df['date'] = df['time'].dt.date

            # Make a copy of the original DF to replace zeros
            df_no_zero = df.copy()

            # Replace 0's with NaN in the 'hr' and 'total_calories' columns
            if all(col in df_no_zero.columns for col in ['hr', 'total_calories']):
                df_no_zero[['hr', 'total_calories']] = df_no_zero[['hr', 'total_calories']].replace(0, np.nan)

                # Group by date and aggregate
                daily_aggregates = df_no_zero.groupby('date').agg({
                    'rr': 'mean',
                    'rrv': 'mean',
                    'steps': 'sum',
                    'hr': ['mean', 'max'],
                    'total_calories': ['sum']
                })

                # Create a unique output filename based on the input file name
                output_filename = os.path.splitext(file_path)[0] + '_daily_aggregates.csv'

                # Save the aggregated results to a CSV file
                daily_aggregates.to_csv(output_filename)

                # Print a message indicating the file was saved
                print(f"Aggregated data saved to: {output_filename}")
            else:
                print(f"Missing required columns in {file_path}. Skipping this file.")

        else:
            print(f"'time' column not found in {file_path}. Skipping this file.")

    except Exception as e: # Error Reporting
        print(f"An error occurred while processing {file_path}: {e}")
print('------------------------------')
print("Processing Complete")
