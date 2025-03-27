import pickle
import re
import sqlite3
import unicodedata
import pandas as pd


def convert_timestamp(x):
    if pd.isnull(x):
        return None
    if isinstance(x, pd.Timestamp):
        return x.isoformat()
    return x


def to_snake_case(name):
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("ASCII")
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    name = name.replace(" ", "_")
    return name.lower()


def clear_sqlite_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}"')
    conn.commit()


def remove_rows_with_large_integers(df):
    threshold = 9223372036854775807
    mask = df.apply(
        lambda col: col.map(lambda x: isinstance(x, int) and abs(x) > threshold)
    )
    rows_to_drop = mask.any(axis=1)
    if rows_to_drop.any():
        indices = df[rows_to_drop].index.tolist()
        for idx in indices:
            print(f"Dropping row {idx} due to an integer exceeding {threshold}")
        df = df.drop(index=indices)
    return df


def pickle_to_sqlite(pickle_file, sqlite_db):
    with open(pickle_file, "rb") as f:
        df = pickle.load(f)
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Pickle file must contain a pandas DataFrame.")
    df.columns = [to_snake_case(col) for col in df.columns]
    for col in df.columns:
        df[col] = df[col].apply(convert_timestamp)
    df = remove_rows_with_large_integers(df)
    conn = sqlite3.connect(sqlite_db)
    clear_sqlite_db(conn)
    df.to_sql("data", conn, if_exists="replace", index=False)
    conn.close()


def main():
    pickle_file = "real_estate_data.pkl"
    sqlite_db = "real_estate_data.db"
    pickle_to_sqlite(pickle_file, sqlite_db)
    print(f"Data successfully converted from {pickle_file} to {sqlite_db}")


if __name__ == "__main__":
    main()
