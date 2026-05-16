# This is the main file for the patient management system. It displays a table of all patients and allows the user to add new patients using a patient intake form.
import dataFunctions
import FreeSimpleGUI as sg
import patientIntakeForm

# Define the table headings and initial data for the patient table
table_headings = [
    "First Name",
    "Last Name",
    "Date of Birth",
    "Height (cm)",
    "Weight (kg)",
    "Taking Medication",
]
# Convert the list of Patient objects to a format suitable for displaying in the table
table_data = dataFunctions.convert_patients_to_table_data(
    patients=dataFunctions.patients
)


# Function to handle the "Add new patient" button click event
def press_add_new_patient_button(patients_window):
    patientIntakeForm.display_patient_intake_form()
    patients_window["PATIENT_TABLE"].update(
        values=dataFunctions.convert_patients_to_table_data(
            patients=dataFunctions.patients
        )
    )


# Create the main window layout for the patient management system
patients_window_layout = [
    [sg.Text("Patient Management System")],
    [sg.Text("All Patient Data"), sg.Button("Add new patient")],
    [
        sg.Table(
            values=table_data,
            headings=table_headings,
            auto_size_columns=True,
            justification="center",
            key="PATIENT_TABLE",
        )
    ],
]

# Create the main window for the patient management system
patients_window = sg.Window("Patient Management System", patients_window_layout)
# Event loop to handle user interactions with the main window
while True:
    event, values = patients_window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Add new patient":
        press_add_new_patient_button(patients_window)
patients_window.close()


"""layout = [
    [sg.Text("tic tac toe example")],
    [sg.Text("x"), sg.Text("o"), sg.Text("x")],
    [sg.Text("o"), sg.Text("o"), sg.Text("x")],
    [sg.Text("x"), sg.Text("x"), sg.Text("o")],
]"""
