
  create or replace   view PATIENTS_SAMPLE.PUBLIC.stg_patients
  
   as (
    

SELECT
    patient_id::INT AS patient_id,
    UPPER(TRIM(first_name)) AS first_name,
    UPPER(TRIM(last_name)) AS last_name,
    TRY_TO_DATE(date_of_birth) AS date_of_birth,
    UPPER(gender) AS gender,
    address,
    phone
FROM PATIENTS_SAMPLE.PUBLIC.PATIENTS
WHERE patient_id IS NOT NULL
  );

