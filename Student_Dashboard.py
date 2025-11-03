import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Generate dataset (1000 random student records)
def generate_student_data(num_records=1000):
    np.random.seed(42)
    genders = ['male', 'female']
    races = ['group A', 'group B', 'group C', 'group D', 'group E']
    educations = ['high school', 'some high school', 'some college', "associate's degree", "bachelor's degree", "master's degree"]
    lunches = ['standard', 'free/reduced']
    preps = ['none', 'completed']

    data = {
        'gender': np.random.choice(genders, num_records),
        'race/ethnicity': np.random.choice(races, num_records),
        'parental level of education': np.random.choice(educations, num_records),
        'lunch': np.random.choice(lunches, num_records),
        'test preparation course': np.random.choice(preps, num_records),
        'math score': np.random.randint(20, 70, num_records),
        'reading score': np.random.randint(20, 70, num_records),
        'writing score': np.random.randint(20, 70, num_records)
    }
    return pd.DataFrame(data)

st.set_page_config(page_title="Student Performance Dashboard", layout="wide", initial_sidebar_state="expanded")

st.title("Student Performance Database")
st.markdown("Search 1000+ student records - **input filters and get output results**")

# Load dataset
all_students = generate_student_data(1000)

# Filter panel
st.sidebar.header("INPUT: Filters")
gender = st.sidebar.selectbox("Gender", options=["", "male", "female"], format_func=lambda x: "All" if x == "" else x)
race = st.sidebar.selectbox("Race/Ethnicity", options=[""] + sorted(all_students['race/ethnicity'].unique()), format_func=lambda x: "All" if x == "" else x)
education = st.sidebar.selectbox("Parental Education", options=[""] + sorted(all_students['parental level of education'].unique()), format_func=lambda x: "All" if x == "" else x)
lunch = st.sidebar.selectbox("Lunch Program", options=["", "standard", "free/reduced"], format_func=lambda x: "All" if x == "" else x)
testPrep = st.sidebar.selectbox("Test Prep", options=["", "none", "completed"], format_func=lambda x: "All" if x == "" else x)

mathMin, mathMax = st.sidebar.slider("Math Score Range", 0, 100, (0,100))
readingMin, readingMax = st.sidebar.slider("Reading Score Range", 0, 100, (0,100))
writingMin, writingMax = st.sidebar.slider("Writing Score Range", 0, 100, (0,100))

# Filter logic
filters = {
    'gender': gender,
    'race/ethnicity': race,
    'parental level of education': education,
    'lunch': lunch,
    'test preparation course': testPrep,
    'mathMin': mathMin,
    'mathMax': mathMax,
    'readingMin': readingMin,
    'readingMax': readingMax,
    'writingMin': writingMin,
    'writingMax': writingMax
}

filtered_students = all_students[
    ((all_students['gender'] == filters['gender']) | (filters['gender'] == "")) &
    ((all_students['race/ethnicity'] == filters['race/ethnicity']) | (filters['race/ethnicity'] == "")) &
    ((all_students['parental level of education'] == filters['parental level of education']) | (filters['parental level of education'] == "")) &
    ((all_students['lunch'] == filters['lunch']) | (filters['lunch'] == "")) &
    ((all_students['test preparation course'] == filters['test preparation course']) | (filters['test preparation course'] == "")) &
    (all_students['math score'] >= filters['mathMin']) & (all_students['math score'] <= filters['mathMax']) &
    (all_students['reading score'] >= filters['readingMin']) & (all_students['reading score'] <= filters['readingMax']) &
    (all_students['writing score'] >= filters['writingMin']) & (all_students['writing score'] <= filters['writingMax'])
]

# Calculate statistics
if filtered_students.shape[0] > 0:
    avgMath = filtered_students['math score'].mean()
    avgReading = filtered_students['reading score'].mean()
    avgWriting = filtered_students['writing score'].mean()

    st.subheader("OUTPUT: Results")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Records Found", filtered_students.shape[0])
    col2.metric("Avg Math", f"{avgMath:.2f}")
    col3.metric("Avg Reading", f"{avgReading:.2f}")
    col4.metric("Avg Writing", f"{avgWriting:.2f}")

    # Bar Chart
    chart_df = pd.DataFrame({
        'Subject': ['Math', 'Reading', 'Writing'],
        'Average': [avgMath, avgReading, avgWriting]
    })
    chart = alt.Chart(chart_df).mark_bar().encode(
        x='Subject',
        y='Average',
        color=alt.Color('Subject', scale=alt.Scale(range=['#3b82f6', '#22c55e', '#f59e42']))
    ).properties(title="Score Distribution", width=500)
    st.altair_chart(chart, use_container_width=True)

    # Records table
    st.subheader(f"All Student Records ({filtered_students.shape[0]} total)")
    st.dataframe(filtered_students.reset_index().rename(columns={"index": "ID"}))
else:
    st.warning("No students match your filters.")

