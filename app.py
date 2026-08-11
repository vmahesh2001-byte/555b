import requests
import streamlit as st

# Configure Page
st.set_page_config(page_title="Student Management Portal", layout="centered")
st.title("🎓 Student Management Portal")

# Backend API Base URL Configuration
API_URL = st.sidebar.text_input("Backend API Base URL", value="http://127.0.0.1:8000")

# Navigation Menu
option = st.sidebar.selectbox(
    "Select Action",
    [
        "View All Students",
        "View Student by ID",
        "Add New Student",
        "Update Student",
        "Delete Student",
    ],
)

# ==============================================================================
# 1. READ ALL STUDENTS
# ==============================================================================
if option == "View All Students":
    st.subheader("📋 All Student Records")

    course_filter = st.text_input(
        "Filter by Course (Optional)", placeholder="e.g., Data Science"
    )

    if st.button("Fetch Students"):
        try:
            params = {"course": course_filter} if course_filter else {}
            response = requests.get(f"{API_URL}/students/", params=params)
            data = response.json()

            if data:
                st.json(data)
            else:
                st.info("No students found.")
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")

# ==============================================================================
# 2. READ SINGLE STUDENT
# ==============================================================================
elif option == "View Student by ID":
    st.subheader("🔍 Search Student by ID")

    student_id = st.number_input("Enter Student ID", min_value=1, step=1)

    if st.button("Get Details"):
        try:
            response = requests.get(f"{API_URL}/students/{student_id}")
            data = response.json()

            if "error" in data:
                st.warning(data["error"])
            else:
                st.success("Student Found!")
                st.json(data)
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")

# ==============================================================================
# 3. CREATE STUDENT (POST)
# ==============================================================================
elif option == "Add New Student":
    st.subheader("➕ Add New Student")

    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=20)
        course = st.text_input("Course Name")

        submit_button = st.form_submit_button("Create Student")

        if submit_button:
            if not name or not course:
                st.warning("Please fill in all fields.")
            else:
                payload = {"name": name, "age": age, "course": course}
                try:
                    response = requests.post(
                        f"{API_URL}/students/", json=payload
                    )
                    st.success("Student created successfully!")
                    st.json(response.json())
                except Exception as e:
                    st.error(f"Connection error: {e}")

# ==============================================================================
# 4. UPDATE STUDENT (PUT)
# ==============================================================================
elif option == "Update Student":
    st.subheader("✏️ Update Existing Student")

    student_id = st.number_input(
        "Enter Student ID to Update", min_value=1, step=1
    )

    with st.form("update_student_form"):
        name = st.text_input("Updated Name")
        age = st.number_input("Updated Age", min_value=1, max_value=100, value=20)
        course = st.text_input("Updated Course")

        submit_button = st.form_submit_button("Update Student")

        if submit_button:
            payload = {"name": name, "age": age, "course": course}
            try:
                response = requests.put(
                    f"{API_URL}/students/{student_id}", json=payload
                )
                data = response.json()

                if "error" in data:
                    st.warning(data["error"])
                else:
                    st.success(f"Student #{student_id} updated successfully!")
                    st.json(data)
            except Exception as e:
                st.error(f"Connection error: {e}")

# ==============================================================================
# 5. DELETE STUDENT (DELETE)
# ==============================================================================
elif option == "Delete Student":
    st.subheader("🗑️ Delete Student Record")

    student_id = st.number_input(
        "Enter Student ID to Delete", min_value=1, step=1
    )

    if st.button("Delete Student", type="primary"):
        try:
            response = requests.delete(f"{API_URL}/students/{student_id}")
            data = response.json()

            if "error" in data:
                st.warning(data["error"])
            else:
                st.success(f"Student #{student_id} deleted successfully!")
                st.json(data)
        except Exception as e:
            st.error(f"Connection error: {e}")