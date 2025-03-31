SELECT
    street_name,
    street_number,
    area_code,
    transaction_date,
    built_area_sqm,
    construction_year,
    declared_transaction_value
FROM transactions
WHERE (? = '' OR street_name LIKE ?)
  AND (? = '' OR street_number = ?)
ORDER BY transaction_date DESC
LIMIT 50;
