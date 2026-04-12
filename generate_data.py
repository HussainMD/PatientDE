import sqlite3
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Number of patients
num_patients = 1000

# Create patients data
patients = []
for i in range(1, num_patients + 1):
    patients.append({
        'patient_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': fake.date_of_birth(minimum_age=0, maximum_age=100),
        'gender': random.choice(['M', 'F']),
        'address': fake.address().replace('\n', ', '),
        'phone': fake.phone_number()
    })

patients_df = pd.DataFrame(patients)

# Create visits data
visits = []
visit_id = 1
for patient in patients:
    num_visits = random.randint(1, 5)
    for _ in range(num_visits):
        visits.append({
            'visit_id': visit_id,
            'patient_id': patient['patient_id'],
            'visit_date': fake.date_between(start_date='-5y', end_date='today'),
            'diagnosis': fake.sentence(nb_words=3),
            'cost': round(random.uniform(50, 5000), 2)
        })
        visit_id += 1

visits_df = pd.DataFrame(visits)

# Connect to SQLite database
conn = sqlite3.connect('healthcare.db')

# Save dataframes to SQL tables
patients_df.to_sql('patients', conn, if_exists='replace', index=False)
visits_df.to_sql('visits', conn, if_exists='replace', index=False)

# Close connection
conn.close()

print("Mock data generated and saved to healthcare.db")