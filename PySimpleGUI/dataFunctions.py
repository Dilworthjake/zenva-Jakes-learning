# This file contains functions for managing patient data, including converting patient data to a format suitable for displaying in a table and creating new patient records from user input.
from datetime import datetime
from patient import Patient

# dummy data for testing
patients = [
    Patient("John", "Doe", datetime(1990, 1, 1), 180, 75.5, False),
    Patient("Jane", "Smith", datetime(1985, 5, 15), 165, 60.2, True),
    Patient("Alice", "Johnson", datetime(1978, 9, 30), 170, 68.9, False),
    Patient("Bob", "Brown", datetime(2000, 12, 20), 190, 115.0, True),
]


# Function to convert a list of Patient objects to a format suitable for displaying in a table
def convert_patients_to_table_data(patients):
    return [patient.convert_values_to_strings() for patient in patients]


# Function to create a new patient record from user input, with validation and error handling
def try_to_create_patient(
    first_name: str,
    last_name: str,
    date_of_birth: str,
    height: str,
    weight: str,
    is_taking_medication,
) -> Patient:
    first_name = first_name.strip()
    last_name = last_name.strip()
    if len(first_name) < 2:
        raise ValueError("First name must contain at least 2 letters.")
    if len(last_name) < 2:
        raise ValueError("Last name must contain at least 2 letters.")
    try:
        date_of_birth = datetime.strptime(date_of_birth.strip(), "%Y-%m-%d")
    except Exception:
        raise ValueError("Date of birth must be YYYY-MM-DD.")
    if date_of_birth > datetime.now():
        raise ValueError("Date of birth cannot be in the future.")
    try:
        height = int(height)
        weight = float(weight)
    except Exception:
        raise ValueError("Height must be an integer and weight must be a number.")
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive.")

    is_taking_medication = bool(is_taking_medication)

    patient = Patient(
        first_name, last_name, date_of_birth, height, weight, is_taking_medication
    )
    patients.append(patient)
    return patient
