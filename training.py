import base64
import streamlit as st
import sqlite3
import pandas as pd
import os

# Tab titles
tabs = ["Input Data", "View Data"]
page = st.sidebar.selectbox("Select a page", tabs)

# Database connection
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Create table
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS user_data(name TEXT, student_number TEXT, gender TEXT)')

# Insert data into table
def add_data(name, student_number, gender):
    c.execute('INSERT INTO user_data(name, student_number, gender) VALUES (?,?,?)', (name, student_number, gender))
    conn.commit()

# Initialize data in table
def init_data():
    c.execute('DELETE FROM user_data')
    conn.commit()

# Export data to CSV
def export_data():
    c.execute('SELECT * FROM user_data')
    data = c.fetchall()
    df = pd.DataFrame(data, columns=["Name", "Student Number", "Gender"])
    csv = df.to_csv(index=False, encoding='cp949')
    # Prompt the user to download the file
    b64 = base64.b64encode(csv.encode('cp949')).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="user_data.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("Data exported to CSV file!")

# Login function
def login():
    st.write("Please login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if username == "admin1" and password == "kanukanu":
        return True
    else:
        return False

# Input data page
if page == "Input Data":
    st.title("Input Data")
    create_table()
    name = st.text_input("Name")
    student_number = st.text_input("Student Number")
    gender = st.radio("Gender", ('Male', 'Female'))
    if st.button("Submit"):
        add_data(name, student_number, gender)
        st.success("Data submitted!")

# View data page
if page == "View Data":
    st.title("View Data")
    if login():
        c.execute('SELECT * FROM user_data')
        data = c.fetchall()
        for row in data:
            st.write(row)
        if st.button("Initialize Data"):
            init_data()
            st.success("Data initialized!")
        if st.button("Export Data"):
            export_data()
