import datetime


class HospitalManagementSystem:
    def __init__(self):
        # In-memory database structures
        self.patients = {}      # ID -> patient details
        self.doctors = {}       # ID -> doctor details
        self.appointments = []  # List of appointment records
        self.patient_counter = 101
        self.doctor_counter = 501

    # --- PATIENT MANAGEMENT ---
    def add_patient(self, name, age, gender, contact):
        patient_id = f"P{self.patient_counter}"
        self.patients[patient_id] = {
            "name": name,
            "age": age,
            "gender": gender,
            "contact": contact,
            "medical_history": []
        }
        self.patient_counter += 1
        print(f"\nSuccess: Patient registered with ID: {patient_id}")

    def view_patients(self):
        if not self.patients:
            print("\nNo patient records found.")
            return
        
        print("\n--- PATIENT LIST ---")
        for p_id, info in self.patients.items():
            print(f"ID: {p_id} | Name: {info['name']} | Age: {info['age']} | Gender: {info['gender']} | Contact: {info['contact']}")

    # --- DOCTOR MANAGEMENT ---
    def add_doctor(self, name, specialization, contact):
        doctor_id = f"D{self.doctor_counter}"
        self.doctors[doctor_id] = {
            "name": name,
            "specialization": specialization,
            "contact": contact
        }
        self.doctor_counter += 1
        print(f"\nSuccess: Doctor registered with ID: {doctor_id}")

    def view_doctors(self):
        if not self.doctors:
            print("\nNo doctor records found.")
            return
            
        print("\n--- DOCTOR LIST ---")
        for d_id, info in self.doctors.items():
            print(f"ID: {d_id} | Name: Dr. {info['name']} | Specialization: {info['specialization']} | Contact: {info['contact']}")

    # --- APPOINTMENT MANAGEMENT ---
    def schedule_appointment(self, patient_id, doctor_id, date_str):
        if patient_id not in self.patients:
            print("\nError: Patient ID not found.")
            return
        if doctor_id not in self.doctors:
            print("\nError: Doctor ID not found.")
            return

        appointment = {
            "appointment_id": len(self.appointments) + 1,
            "patient_id": patient_id,
            "patient_name": self.patients[patient_id]["name"],
            "doctor_id": doctor_id,
            "doctor_name": self.doctors[doctor_id]["name"],
            "date": date_str
        }
        self.appointments.append(appointment)
        print(f"\nSuccess: Appointment booked (ID: {appointment['appointment_id']})")

    def view_appointments(self):
        if not self.appointments:
            print("\nNo scheduled appointments found.")
            return
            
        print("\n--- APPOINTMENTS ---")
        for app in self.appointments:
            print(f"ID: {app['appointment_id']} | Date: {app['date']} | Patient: {app['patient_name']} ({app['patient_id']}) -> Doctor: Dr. {app['doctor_name']} ({app['doctor_id']})")

    # --- MEDICAL HISTORY ---
    def add_medical_record(self, patient_id, diagnosis, prescription):
        if patient_id not in self.patients:
            print("\nError: Patient ID not found.")
            return

        record = {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "diagnosis": diagnosis,
            "prescription": prescription
        }
        self.patients[patient_id]["medical_history"].append(record)
        print(f"\nSuccess: Medical record added for {self.patients[patient_id]['name']}")

    def view_patient_history(self, patient_id):
        if patient_id not in self.patients:
            print("\nError: Patient ID not found.")
            return

        patient = self.patients[patient_id]
        print(f"\n--- MEDICAL HISTORY FOR {patient['name']} ({patient_id}) ---")
        if not patient["medical_history"]:
            print("No medical records available.")
            return

        for idx, rec in enumerate(patient["medical_history"], 1):
            print(f"{idx}. Date: {rec['date']} | Diagnosis: {rec['diagnosis']} | Prescription: {rec['prescription']}")


# --- INTERACTIVE MENU ---
def main():
    hms = HospitalManagementSystem()
    
    # Pre-populating dummy data for ease of use
    hms.add_doctor("Alice Smith", "Cardiology", "555-0100")
    hms.add_doctor("Bob Jones", "Pediatrics", "555-0101")
    hms.add_patient("John Doe", 30, "Male", "555-0200")

    while True:
        print("\n=================================")
        print("    HOSPITAL MANAGEMENT SYSTEM   ")
        print("=================================")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Schedule Appointment")
        print("6. View Appointments")
        print("7. Add Medical Record")
        print("8. View Patient Medical History")
        print("9. Exit")
        
        choice = input("\nEnter choice (1-9): ").strip()

        if choice == "1":
            name = input("Enter Patient Name: ")
            age = input("Enter Age: ")
            gender = input("Enter Gender: ")
            contact = input("Enter Contact Number: ")
            hms.add_patient(name, age, gender, contact)

        elif choice == "2":
            hms.view_patients()

        elif choice == "3":
            name = input("Enter Doctor Name: ")
            spec = input("Enter Specialization: ")
            contact = input("Enter Contact Number: ")
            hms.add_doctor(name, spec, contact)

        elif choice == "4":
            hms.view_doctors()

        elif choice == "5":
            p_id = input("Enter Patient ID (e.g., P101): ").upper()
            d_id = input("Enter Doctor ID (e.g., D501): ").upper()
            date = input("Enter Date (YYYY-MM-DD): ")
            hms.schedule_appointment(p_id, d_id, date)

        elif choice == "6":
            hms.view_appointments()

        elif choice == "7":
            p_id = input("Enter Patient ID: ").upper()
            diagnosis = input("Enter Diagnosis: ")
            prescription = input("Enter Prescription Details: ")
            hms.add_medical_record(p_id, diagnosis, prescription)

        elif choice == "8":
            p_id = input("Enter Patient ID: ").upper()
            hms.view_patient_history(p_id)

        elif choice == "9":
            print("\nExiting System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
