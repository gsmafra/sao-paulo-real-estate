import os
import pandas as pd
from tqdm import tqdm


def clear_pickle_file(pickle_file):
    """Clears the pickle file by deleting it if it exists."""
    if os.path.exists(pickle_file):
        os.remove(pickle_file)


def disambiguate_acc_columns(df_sheet):
    """For every column named 'ACC (IPTU)' in a sheet:
    - If at least 99% of the rows are numeric (or null), convert non-numeric values to null and keep the name.
    - Otherwise, rename it to 'Descrição do padrão (IPTU)'.
    Raises an error if duplicate column names are found after processing."""
    columns = df_sheet.columns.tolist()
    for idx, col in enumerate(columns):
        if col == "ACC (IPTU)":
            series_col = df_sheet.iloc[:, idx]
            valid = series_col.apply(
                lambda x: pd.isna(x) or not pd.isna(pd.to_numeric(x, errors="coerce"))
            )
            fraction_numeric = valid.sum() / len(series_col)
            if fraction_numeric >= 0.99:
                converted_series = pd.to_numeric(series_col, errors="coerce")
                df_sheet.iloc[:, idx] = converted_series
                columns[idx] = "ACC (IPTU)"  # remains numeric
            else:
                columns[idx] = "Descrição do padrão (IPTU)"
    df_sheet.columns = columns
    duplicates = [col for col in set(columns) if columns.count(col) > 1]
    assert (
        len(duplicates) == 0
    ), f"Duplicate column names found in dataframe: {duplicates}"
    return df_sheet


def process_excel_file(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    excel_file = pd.ExcelFile(file_path, engine="openpyxl")
    dfs_sheets = []
    for sheet_name in excel_file.sheet_names:
        if base_name in sheet_name:
            df_sheet = excel_file.parse(sheet_name)
            df_sheet = disambiguate_acc_columns(df_sheet)
            df_sheet = df_sheet.rename(columns={"ACC (IPTU).1": "ACC (IPTU)"})
            dfs_sheets.append(df_sheet)
    return dfs_sheets


def process_specific_excel_files(file_paths, pickle_file):
    dfs_sheets = []
    for file_path in tqdm(file_paths):
        dfs_sheets.extend(process_excel_file(file_path))
    df_complete = pd.concat(dfs_sheets, ignore_index=True)
    df_complete.to_pickle(pickle_file)


def process_excel_files(data_dir, pickle_file):
    file_paths = [
        os.path.join(data_dir, file_name)
        for file_name in os.listdir(data_dir)
        if file_name.endswith(".xlsx")
    ]
    process_specific_excel_files(file_paths, pickle_file)


def main():
    data_dir = "data/raw"
    pickle_file = os.path.join("data/interim", "real_estate_data.pkl")
    clear_pickle_file(pickle_file)
    process_excel_files(data_dir, pickle_file)


if __name__ == "__main__":
    main()
