import pickle
import sqlite3
import pandas as pd
import re
import unicodedata

def convert_timestamp(x):
    if pd.isnull(x):
        return None
    if isinstance(x, pd.Timestamp):
        return x.isoformat()
    return x

def to_snake_case(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
    name = name.replace(' ', '_')
    return name.lower()

def clear_sqlite_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute('DROP TABLE IF EXISTS "{}"'.format(table[0]))
    conn.commit()

def detect_large_integers(df):
    threshold = 9223372036854775807
    for col in df.columns:
        for idx, val in df[col].items():
            if isinstance(val, int) and abs(val) > threshold:
                print(f"Large integer found at row {idx}, column '{col}': {val}")

def remove_rows_with_large_integers(df):
    threshold = 9223372036854775807
    mask = df.applymap(lambda x: isinstance(x, int) and abs(x) > threshold)
    rows_to_drop = mask.any(axis=1)
    if rows_to_drop.any():
        indices = df[rows_to_drop].index.tolist()
        for idx in indices:
            print(f"Dropping row {idx} due to an integer exceeding {threshold}")
        df = df.drop(index=indices)
    return df

def pickle_to_sqlite(pickle_file, sqlite_db):
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Pickle file must contain a pandas DataFrame.")
    data.columns = [to_snake_case(col) for col in data.columns]
    for col in data.columns:
        data[col] = data[col].apply(convert_timestamp)
    detect_large_integers(data)
    data = remove_rows_with_large_integers(data)
    conn = sqlite3.connect(sqlite_db)
    clear_sqlite_db(conn)
    data.to_sql('data', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    pickle_file = "real_estate_data.pkl"
    sqlite_db = "real_estate_data.db"
    try:
        pickle_to_sqlite(pickle_file, sqlite_db)
        print(f"Data successfully converted from {pickle_file} to {sqlite_db}")
    except Exception as e:
        print(f"Error: {e}")
