SELECT
    *,
    CAST(CURRENT_TIMESTAMP AS DATETIME) AS uploaded_at
FROM
    {table_name}
ORDER BY
    id