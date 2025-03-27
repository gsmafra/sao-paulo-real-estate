import os
import pandas as pd
from tqdm import tqdm

def clear_pickle_file(pickle_file):
    """Clears the pickle file by deleting it if it exists."""
    if os.path.exists(pickle_file):
        os.remove(pickle_file)

def disambiguate_acc_columns(df):
    """For every column named 'ACC (IPTU)':
    - If at least 99% of its rows are numeric (or null), convert non-numeric values to null and keep the name.
    - Otherwise, rename it to 'Descrição do padrão (IPTU)'.
    Raises an error if duplicate column names are found after processing."""
    columns = df.columns.tolist()
    for idx, col in enumerate(columns):
        if col == "ACC (IPTU)":
            series = df.iloc[:, idx]
            # Determine numeric validity: an entry is valid if it is null or numeric.
            valid = series.apply(lambda x: pd.isna(x) or not pd.isna(pd.to_numeric(x, errors="coerce")))
            fraction_numeric = valid.sum() / len(series)
            if fraction_numeric >= 0.99:
                # Convert non-numeric values to null.
                converted = pd.to_numeric(series, errors="coerce")
                df.iloc[:, idx] = converted
                columns[idx] = "ACC (IPTU)"  # remains numeric
            else:
                columns[idx] = "Descrição do padrão (IPTU)"
    df.columns = columns
    duplicates = [col for col in set(columns) if columns.count(col) > 1]
    assert len(duplicates) == 0, f"Duplicate column names found in dataframe: {duplicates}"
    return df

def process_excel_file(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    excel_file = pd.ExcelFile(file_path, engine="openpyxl")
    dfs = []
    for sheet_name in excel_file.sheet_names:
        if base_name in sheet_name:
            df = excel_file.parse(sheet_name)
            try:
                df = disambiguate_acc_columns(df)
            except AssertionError as ae:
                raise AssertionError(f"Error processing file '{file_path}', sheet '{sheet_name}': {ae}")
            df = df.rename(columns={"ACC (IPTU).1": "ACC (IPTU)"})
            dfs.append(df)
    return dfs

def process_specific_excel_files(file_paths, pickle_file):
    all_data = []
    for file_path in tqdm(file_paths):
        all_data.extend(process_excel_file(file_path))
    combined_data = pd.concat(all_data, ignore_index=True)
    combined_data.to_pickle(pickle_file)

def process_excel_files(data_dir, pickle_file):
    file_paths = [
        os.path.join(data_dir, file_name)
        for file_name in os.listdir(data_dir)
        if file_name.endswith(".xlsx")
    ]
    process_specific_excel_files(file_paths, pickle_file)

def main():
    data_dir = "data/"
    pickle_file = "real_estate_data.pkl"
    clear_pickle_file(pickle_file)
    process_excel_files(data_dir, pickle_file)

if __name__ == "__main__":
    main()
