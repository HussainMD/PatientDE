  # Patient Data Pipeline

  This project scaffolds an end-to-end patient data pipeline.

  ## Components

  - **generate_data.py**: Generates mock patient and visit data using Faker and saves to SQLite database `healthcare.db`.
  - **upload_to_snowflake.py**: Uploads data from SQLite to Snowflake database `PATEINTS_SAMPLE` in schema `PUBLIC`.
  - **dbt/**: dbt project for data transformations.
    - `src_healthcare.yml`: Defines source tables.
    - `stg_patients.sql`: Staging model for patients with type casting and cleanup.
    - `fct_patient_history.sql`: Mart model calculating total spend per patient.

  ## Setup

  1. Update `.env` with your Snowflake credentials.
  2. Run `python generate_data.py` to create mock data.
  3. Run `python upload_to_snowflake.py` to upload to Snowflake.
  4. In `dbt/` directory, run `dbt run` to execute transformations.

  ## Requirements

  See `requirements.txt` for Python dependencies.