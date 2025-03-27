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


def preprocess_data(df):
    # Rename and convert the transaction value column
    df = df.rename(
        columns={"valor_de_transacao_declarado_pelo_contribuinte": "transaction_value"}
    )
    df["transaction_value"] = pd.to_numeric(df["transaction_value"], errors="coerce")

    n_invalid = df["transaction_value"].isna().sum()
    if n_invalid:
        print(f"Removed {n_invalid} rows due to non-convertible transaction_value.")
    df = df.dropna(subset=["transaction_value"])
    df = df[df["transaction_value"] <= 20_000_000]

    # Preserve the cleaned original data for later display.
    df_original = df.copy()

    # Prepare transformed features for model training.
    # Exclude the description's original text so that only numeric features remain.
    df_features = df[["acc_iptu", "area_construida_m2", "cep"]].copy()

    # Clean and label-encode the description column separately.
    descricao_clean = (
        df["descricao_do_padrao_iptu"]
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", "", regex=True)
        .str.lower()
    )
    # Label encode the cleaned descriptions.
    descricao_encoded = descricao_clean.astype("category").cat.codes
    df_features["descricao_do_padrao_iptu"] = descricao_encoded

    y = df["transaction_value"]
    return df_original, df_features, y


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
    db_path = "real_estate_data.db"
    query = """
    SELECT
        acc_iptu,
        area_construida_m2,
        cep,
        descricao_do_padrao_iptu,
        valor_de_transacao_declarado_pelo_contribuinte
    FROM data
    """

    # Load data from the database and preprocess it,
    # obtaining both the original and transformed feature DataFrames.
    df_original, df_features, y = preprocess_data(load_data(db_path, query))

    # Split the transformed data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        df_features, y, test_size=0.2, random_state=42
    )

    print("Training with features:", x_train.columns.tolist())
    model = train_model(x_train, y_train)

    rmse = evaluate_model(model, x_test, y_test)
    print(f"RMSE: {rmse}")

    # Display sample test predictions using the original data
    display_sample_predictions(model, x_test, df_original)


if __name__ == "__main__":
    main()
