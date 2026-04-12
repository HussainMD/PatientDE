{{ config(materialized='table') }}

SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    p.date_of_birth,
    p.gender,
    COUNT(v.visit_id) AS total_visits,
    SUM(v.cost) AS total_spend
FROM {{ ref('stg_patients') }} p
LEFT JOIN {{ source('healthcare_raw', 'VISITS') }} v ON p.patient_id = v.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name, p.date_of_birth, p.gender