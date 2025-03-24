import os
import pandas as pd
from tqdm import tqdm

def clear_pickle_file(pickle_file):
    """Clears the pickle file by deleting it if it exists."""
    if os.path.exists(pickle_file):
        os.remove(pickle_file)

def process_excel_files(data_dir, pickle_file):
    """Processes Excel files in the specified directory and saves data to a pickle file."""
    all_data = []

    for file_name in tqdm(os.listdir(data_dir)):
        if not file_name.endswith(".xlsx"):
            continue
        file_path = os.path.join(data_dir, file_name)
        base_name = os.path.splitext(file_name)[0]

        excel_file = pd.ExcelFile(file_path, engine="openpyxl")

        for sheet_name in excel_file.sheet_names:
            if base_name in sheet_name:
                df = excel_file.parse(sheet_name)
                all_data.append(df)

    # Concatenate all dataframes, aligning columns
    combined_data = pd.concat(all_data, ignore_index=True)

    # Save to the pickle file
    combined_data.to_pickle(pickle_file)

def main():
    data_dir = "data/"
    pickle_file = "real_estate_data.pkl"

    clear_pickle_file(pickle_file)
    process_excel_files(data_dir, pickle_file)

if __name__ == "__main__":
    main()
