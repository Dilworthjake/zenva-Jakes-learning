# This file defines the patient intake form for the patient management system. It contains functions to create and display the form, as well as to read and validate the input values from the form.
import FreeSimpleGUI as sg
import dataFunctions


# Function to read and validate the input values from the patient intake form
def read_input_values(values):
    first_name = values["FIRST_NAME"]
    last_name = values["LAST_NAME"]
    date_of_birth = values["DATE_OF_BIRTH"]
    height = values["HEIGHT"]
    weight = values["WEIGHT"]
    is_taking_medication = values["IS_TAKING_MEDICATION"]
    try:
        dataFunctions.try_to_create_patient(
            first_name, last_name, date_of_birth, height, weight, is_taking_medication
        )
        return True
    except ValueError as e:
        sg.popup_error(str(e))
        return False


# Function to create the layout for the patient intake form
def create_patient_intake_form():
    return [
        [sg.Text("First Name"), sg.Input(key="FIRST_NAME")],
        [sg.Text("Last Name"), sg.Input(key="LAST_NAME")],
        [
            sg.Text("Date of Birth"),
            sg.Input(key="DATE_OF_BIRTH"),
            sg.CalendarButton("Select Date", target="DATE_OF_BIRTH", format="%Y-%m-%d"),
        ],
        [sg.Text("Height (cm)"), sg.Input(key="HEIGHT")],
        [sg.Text("Weight (kg)"), sg.Input(key="WEIGHT")],
        [
            sg.Text("Taking Medication"),
            sg.Checkbox("Yes", key="IS_TAKING_MEDICATION", default=False),
        ],
        [sg.Cancel("Cancel"), sg.Button("Save")],
    ]


# Function to display the patient intake form and handle user interactions with the form
def display_patient_intake_form():
    patient_intake_form_layout = create_patient_intake_form()
    patient_intake_window = sg.Window("Patient Intake Form", patient_intake_form_layout)

    while True:
        event, values = patient_intake_window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break
        elif event == "Save":
            success = read_input_values(values)
            if success:
                break

    patient_intake_window.close()
