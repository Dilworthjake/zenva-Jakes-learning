welcome_prompt = "Welcome to the dehydration assessment tool!, what will you like to do? \n - To list all patients, press 1 \n - To run a new assessment, press 2 \n - To quit press q\n"

name_prompt = "Please enter the patient's name: \n"

appearance_prompt = "How is the patient's appearance? \n - 1: Normal appearance \n - 2: Irritable or lethargic \n"

eye_prompt = "How are the patient's eyes? \n - 1: Eyes normal or slightly sunken \n - 2: Eyes very sunken \n"

skin_prompt = "How is the patient's skin turgor? \n - 1: Skin returns to normal immediately \n - 2: Skin returns to normal slowly (after more than 2 seconds) \n"

severe_dehydration = "severely dehydrated"
some_dehydration = "some dehydration"
no_dehydration = "no dehydration"


patients_and_diagnoses = [
    "John Doe - some dehydration",
    "Jane Smith - severely dehydrated",
    "Alice Johnson - no dehydration",
]


def save_patient_diagnosis(patient_name, diagnosis):
    if patient_name == "" or diagnosis == "":
        print("Patient name and diagnosis cannot be empty. Please try again.")
        return
    final_diagnosis = f"{patient_name} - {diagnosis}"
    patients_and_diagnoses.append(final_diagnosis)
    print(f"Saved diagnosis for {patient_name}: {diagnosis} \n")


def list_patients():
    print("Listing all patients... \n")
    for patient in patients_and_diagnoses:
        print(patient)


def assess_skin(skin):
    if skin == "1":
        return some_dehydration
    elif skin == "2":
        return severe_dehydration
    else:
        return "Invalid skin selection"


def assess_eyes(eyes):
    if eyes == "1":
        return no_dehydration
    elif eyes == "2":
        return severe_dehydration
    else:
        return "Invalid eye selection"


def diagnosis_appearance():
    appearance = input(appearance_prompt)
    if appearance == "1":
        eyes = input(eye_prompt)
        return assess_eyes(eyes)
    elif appearance == "2":
        skin = input(skin_prompt)
        return assess_skin(skin)
    else:
        return "Invalid appearance selection"


def run_new_assessment():
    print("Running new assessment... \n")
    patient_name = input(name_prompt)
    diagnosis = diagnosis_appearance()
    save_patient_diagnosis(patient_name, diagnosis)


def main():
    while True:
        selection = input(welcome_prompt)
        if selection == "1":
            list_patients()
        elif selection == "2":
            run_new_assessment()
        elif selection == "q":
            print("Quitting... \n")
            return
        else:
            print("Invalid selection. Please try again. \n")


# main()


def test_assess_skin():
    assert assess_skin("1") == some_dehydration
    assert assess_skin("2") == severe_dehydration
    assert assess_skin("") == "Invalid skin selection"
    print("assess_skin tests passed!")


# test_assess_skin()


def test_assess_eyes():
    assert assess_eyes("1") == no_dehydration
    assert assess_eyes("2") == severe_dehydration
    assert assess_eyes("") == "Invalid eye selection"
    print("assess_eyes tests passed!")


# test_assess_eyes()
