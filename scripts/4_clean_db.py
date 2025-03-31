import sqlite3
import pandas as pd

# Configuration: Column mapping
COLUMN_MAP = {
    "n_do_cadastro_sql": "property_id",
    "nome_do_logradouro": "street_name",
    "numero": "street_number",
    "complemento": "complement",
    "bairro": "neighborhood",
    "referencia": "reference",
    "cep": "area_code",
    "natureza_de_transacao": "transaction_type",
    "valor_de_transacao_declarado_pelo_contribuinte": "declared_transaction_value",
    "data_de_transacao": "transaction_date",
    "tipo_de_financiamento": "financing_type",
    "valor_financiado": "financed_amount",
    "area_do_terreno_m2": "land_area_sqm",
    "area_construida_m2": "built_area_sqm",
    "descricao_do_uso_iptu": "usage_type_description",
    "descricao_do_padrao_iptu": "standard_type_description",
    "acc_iptu": "construction_year",
}


def main():
    db_path = "data/final/real_estate_data.db"
    conn = sqlite3.connect(db_path)
    print("Database connection opened successfully.")

    # Pull raw data into memory.
    df = pd.read_sql_query("SELECT * FROM raw_transactions", conn)
    print("Data loaded to memory.")

    # Drop any columns that are not in COLUMN_MAP.
    df = df[list(COLUMN_MAP.keys())]

    # Convert transaction_date (data_de_transacao) to datetime and drop time portion.
    df["data_de_transacao"] = pd.to_datetime(
        df["data_de_transacao"], errors="coerce"
    ).dt.date

    # Rename columns according to COLUMN_MAP.
    df = df.rename(columns=COLUMN_MAP)

    # Save the transformed data into a new table 'transactions'
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    print("Table 'transactions' created successfully.")

    conn.close()


if __name__ == "__main__":
    main()
