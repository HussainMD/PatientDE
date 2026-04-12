{{ config(materialized='view') }}

SELECT
    patient_id::INT AS patient_id,
    UPPER(TRIM(first_name)) AS first_name,
    UPPER(TRIM(last_name)) AS last_name,
    TRY_TO_DATE(date_of_birth) AS date_of_birth,
    UPPER(gender) AS gender,
    address,
    phone
FROM {{ source('healthcare_raw', 'patients') }}
WHERE patient_id IS NOT NULL