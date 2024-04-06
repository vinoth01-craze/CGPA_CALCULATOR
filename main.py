import streamlit as st
import pandas as pd
import base64
import numpy as np

grade_values = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'RA': 0, 'AB': 0}

st.set_page_config(
    page_title="CGPA Calculator",
    page_icon=":bar_chart:",
    layout="wide",  # or "centered"
    initial_sidebar_state="collapsed"  # or "expanded"
)

# Function to create an empty template CSV file
def create_empty_template(num_subjects, num_students, semester, i=0):
    # Create DataFrame with grade columns
    grade_columns = [f'Grade{i}_{semester}' for i in range(num_subjects)]
    template_data_grade = {
        'Reg. No.': [],
        'Student Name': [],
    }
    for col in grade_columns:
        template_data_grade[col] = []
    df_grade = pd.DataFrame(template_data_grade)

    # Create DataFrame with credit columns
    credit_columns = [f'Credit{i}_{semester}' for i in range(1, num_subjects + 1)]
    template_data_credit = {col: [] for col in credit_columns}
    df_credit = pd.DataFrame(template_data_credit)

    # Concatenate grade and credit DataFrames
    df_template = pd.concat([df_grade, df_credit], axis=1)

    # Fill credit values for all students
    for col in credit_columns:
        i+=1
        credit_value = st.number_input(f'Enter credit value for subject{i}:', min_value=0, value=0, step=1, key=f'{col}_input')
        df_template[col] = [credit_value] * num_students

    # Fill student names range
    for i in range(num_students):
        df_template.loc[i, 'Reg. No.'] = np.nan
        df_template.loc[i, 'Student Name'] = np.nan

    return df_template

def calculate_gpa(row):
    total_credit_points = 0
    total_credits = 0
    arrear_count = 0
    absent_count = 0
    gpa = np.nan  # Default GPA to NaN

    for col in row.index:
        if 'Grade' in col:
            grade_col = col
            credit_col = col.replace('Grade', 'Credit')
            # Check if the credit column exists
            if credit_col in row.index:
                grade = row[grade_col]
                credit = row[credit_col]
                # Handle 'RA' or 'AB' grades
                if grade == 'RA':
                    arrear_count += 1
                elif grade == 'AB':
                    absent_count += 1
                else:
                    # Convert grade to its corresponding integer value
                    grade_value = grade_values.get(grade, 0)
                    # Ensure credit is converted to int type
                    credit_value = int(credit)
                    total_credit_points += grade_value * credit_value
                    total_credits += credit_value
    if arrear_count == 0 and absent_count == 0:
        gpa = total_credit_points / total_credits if total_credits != 0 else 0

    return gpa, arrear_count, absent_count

def main():
    uploaded_files = []  # Initialize uploaded_files list

    # Custom CSS to set background image
    st.markdown(
        """
        <style>
        .stTextInput>div>div>input[type="number"] {
            width: 1000px !important; /* Adjust width of number input box */
            background-color: white !important; /* Set background color to white */
        }
        h1 {
            width: 400px;
            padding: 0%;
            top: 5%;
            left: 40%;
            font-size: 60px;
            color: lightwhite;
            font-family: Garamond, serif;
            white-space: nowrap; /* Ensures text stays on a single line */
            -webkit-animation: glow 1s ease-in-out infinite alternate;
            -moz-animation: glow 1s ease-in-out infinite alternate;
            animation: glow 1s ease-in-out infinite alternate;
            margin-bottom: 100px;
            background-clip: padding-box;
            box-shadow: 0 0 50px white;
        }
        h2{
            color:lightblue;
            font-family: Copperplate, Papyrus, fantasy;
        }
        h3{
            color:yellow;
          font-family: Copperplate, Papyrus, fantasy;
        }
        P {
            color: white;
            font-family: Copperplate, Papyrus, fantasy;
        }
        .stButton>button {
            background-color: black; /* Background color of the button */
        }
        .stButton>button:hover {
            cursor: pointer;
        }
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1598690042638-1b9844b7ef83?q=80&w=2065&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            object-fit:center;
        }
        @-webkit-keyframes glow {
            from {
                text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #e60073, 0 0 40px #e60073, 0 0 50px #e60073, 0 0 60px #e60073, 0 0 70px #e60073;
            }
            to {
                text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6, 0 0 50px #ff4da6, 0 0 60px #ff4da6, 0 0 70px #ff4da6, 0 0 80px #ff4da6;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("GPA  and  CGPA CALCULATOR - INFO TECH  :books:")

    # Input number of semesters
    num_semesters = st.number_input("Enter the number of semesters:", min_value=0, value=0, step=1)

    # Allow users to download an empty template CSV file for each semester
    for semester in range(num_semesters):
        st.markdown(f"## Sem {semester+1}")
        num_subjects = st.number_input(f"Enter the number of subjects for Semester {semester+1}:", min_value=0, value=0,
                                       step=1)
        if num_subjects > 0:
            num_students = st.number_input(f"Enter the number of students for Semester {semester+1}:", min_value=0,
                                           value=0,
                                           step=1)
            template_df = create_empty_template(num_subjects, num_students, semester)  # Pass the semester parameter
            st.markdown(f"### Download an empty template CSV file for Semester {semester+1}:")
            csv_template = template_df.to_csv(index=False)
            b64_template = base64.b64encode(csv_template.encode()).decode()  # Convert to base64
            href_template = f'<a href="data:file/csv;base64,{b64_template}" download="Semester_{semester+1}_Template.csv">Download Semester {semester+1} Template CSV File</a>'
            st.markdown(href_template, unsafe_allow_html=True)
            st.write("")

        # Allow users to upload CSV files for each semester
    uploaded_files = []
    for semester in range(num_semesters):
        if num_subjects !=0:
            uploaded_file = st.file_uploader(f"Upload CSV file for Semester {semester + 1}", type="csv")
            if uploaded_file is not None:
                uploaded_files.append(pd.read_csv(uploaded_file))

    if num_semesters != 0 and num_subjects != 0 and len(uploaded_files) == num_semesters and st.button("Calculate GPA and CGPA"):
        # Initialize DataFrame to store all GPA values
        df_gpas = []

        # Combine all uploaded files
        for i, df in enumerate(uploaded_files, start=1):
            df['GPA - {}'.format(i)], df['Arrear - {}'.format(i)], df['Absent - {}'.format(i)] = zip(
                *df.apply(calculate_gpa, axis=1))
            df_gpas.append(df[['Reg. No.', 'Student Name', 'GPA - {}'.format(i), 'Arrear - {}'.format(i),
                               'Absent - {}'.format(i)]])
            st.write(f"### Semester {i} Results")
            st.write(df_gpas[-1])

        # Merge data from all semesters based on 'Reg. No.' and 'Student Name'
        df_combined = df_gpas[0]
        for df_gpa in df_gpas[1:]:
            df_combined = pd.merge(df_combined, df_gpa, on=['Reg. No.', 'Student Name'], how='outer')

        # Calculate CGPA for each student
        df_combined['CGPA'] = df_combined.filter(like='GPA').mean(axis=1)

        # Exclude students with absences in any semester from CGPA calculation
        df_combined.loc[(df_combined.filter(like='Absent').sum(axis=1) > 0), 'CGPA'] = np.nan

        # Exclude students with arrears in any semester from CGPA calculation
        df_combined.loc[(df_combined.filter(like='Arrear').sum(axis=1) > 0), 'CGPA'] = np.nan

        # Create CSV file for download
        csv_file = df_combined.to_csv(index=False)
        b64 = base64.b64encode(csv_file.encode()).decode()  # Convert to base64
        href = f'<a href="data:file/csv;base64,{b64}" download="GPA_CGPA_Result.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Display combined data with GPA and CGPA
        st.write("### OverAll CGPA:")
        # Display only 'Reg. No.', 'Student Name', and 'CGPA' columns
        st.write(df_combined[['Reg. No.', 'Student Name', 'CGPA']])

        # Display top three CGPA scorers with only 'Reg. No.', 'Student Name', and 'CGPA' columns
        st.write("### Top three CGPA scorers:")
        top_three_scorers = df_combined.nlargest(3, 'CGPA')[['Reg. No.', 'Student Name', 'CGPA']]
        st.write(top_three_scorers)

if __name__ == "__main__":
    main()