import streamlit as st
import sqlite3

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
