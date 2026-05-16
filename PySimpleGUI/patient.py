# This file defines the Patient class, which represents a patient in the patient management system. The Patient class has attributes for the patient's first name, last name, date of birth, height, weight, and whether they are taking medication. It also has a method to convert the patient's data into a format suitable for displaying in a table.
from datetime import datetime


class Patient:
    def __init__(
        self,
        first_name,
        last_name,
        date_of_birth,
        height,
        weight,
        is_taking_medication=False,
    ):
        # Initialize the Patient object with the provided attributes
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.height = height
        self.weight = weight
        self.is_taking_medication = is_taking_medication

    # Method to convert the patient's data into a format suitable for displaying in a table
    def convert_values_to_strings(self):
        date_of_birth = self.date_of_birth.strftime("%Y-%m-%d")
        height = str(self.height)
        weight = str(self.weight)
        is_taking_medication = "Yes" if self.is_taking_medication else "No"

        return [
            self.first_name,
            self.last_name,
            date_of_birth,
            height,
            weight,
            is_taking_medication,
        ]
