import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_data(db_path, query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def preprocess_original(df):
    # Convert the reported transaction value column to numeric.
    df["reported_transaction_value"] = pd.to_numeric(
        df["reported_transaction_value"], errors="coerce"
    )

    n_invalid = df["reported_transaction_value"].isna().sum()
    if n_invalid:
        print(f"Removed {n_invalid} rows due to non-convertible reported_transaction_value.")
    df = df.dropna(subset=["reported_transaction_value"])
    df = df[df["reported_transaction_value"] <= 20_000_000]

    # Return the cleaned original data.
    return df.copy()


def transform_features(df_original):
    # Prepare transformed features for model training using the SQL alias names.
    df_features = df_original[["construction_year", "contructed_area", "area_code"]].copy()

    # Clean and label-encode the property description column.
    property_desc_clean = (
        df_original["property_description"]
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", "", regex=True)
        .str.lower()
    )
    property_desc_encoded = property_desc_clean.astype("category").cat.codes
    df_features["property_description"] = property_desc_encoded

    # The target variable is the reported transaction value.
    y = df_original["reported_transaction_value"]

    return df_features, y


def train_model(x_train, y_train):
    model = RandomForestRegressor(random_state=42, max_depth=5, n_estimators=20)
    model.fit(x_train, y_train)
    return model


def evaluate_model(model, x_test, y_test):
    y_pred = model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return rmse


def display_sample_predictions(model, x_test, df_original, sample_size=5):
    # Choose a random sample of indices from the test set.
    sample_indices = np.random.choice(x_test.index, size=sample_size, replace=False)

    # Predictions based on transformed features.
    x_sample = x_test.loc[sample_indices]
    predictions = model.predict(x_sample)

    # Retrieve the corresponding original data for display.
    sample_original = df_original.loc[sample_indices].copy()
    # Format the predicted values to two decimals.
    sample_original["Predicted Value"] = [f"{pred:.2f}" for pred in predictions]

    print("\nSample Test Cases (from original data):")
    print(sample_original)


def main():
    db_path = "data/final/real_estate_data.db"
    query = """
    SELECT
        acc_iptu AS construction_year,
        area_construida_m2 AS contructed_area,
        cep AS area_code,
        descricao_do_padrao_iptu AS property_description,
        valor_de_transacao_declarado_pelo_contribuinte AS reported_transaction_value
    FROM data
    """

    # Load data from the database.
    df_loaded = load_data(db_path, query)

    # Preprocess the original data.
    df_original = preprocess_original(df_loaded)

    # Transform features from the preprocessed original data.
    df_features, y = transform_features(df_original)

    # Split the transformed data into training and testing sets.
    x_train, x_test, y_train, y_test = train_test_split(
        df_features, y, test_size=0.2, random_state=42
    )

    print("Training with features:", x_train.columns.tolist())
    model = train_model(x_train, y_train)

    rmse = evaluate_model(model, x_test, y_test)
    print(f"RMSE: {rmse}")

    # Display sample test predictions using the original data.
    display_sample_predictions(model, x_test, df_original)


if __name__ == "__main__":
    main()
