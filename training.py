import base64
import streamlit as st
import sqlite3
import pandas as pd


# Tab titles
tabs = ["시실리 활동 신청", "신청 내역 확인"]
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
    st.success("엑셀 파일로 저장되었어요!")

# Login function
def login():
    st.write("로그인이 필요합니다")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if username == "admin1" and password == "kanukanu":
        return True
    elif username != "admin1" or password != "kanukanu":
        st.error ("아이디 또는 비밀번호가 틀렸습니다.")
        return False
    else:
        return False

# Input data page
if page == "시실리 활동 신청":
    st.title("시실리 활동 신청")
    create_table()
    name = st.text_input("이름")
    student_number = st.text_input("학번")
    gender = st.radio("성별", ('남', '여'))
    if st.button("신청하기"):
        add_data(name, student_number, gender)
        st.success("신청되었습니다!")

# View data page
if page == "신청 내역 확인":
    st.title("신청 내역 확인")
    if login():
        c.execute('SELECT * FROM user_data')
        data = c.fetchall()
        for row in data:
            st.write(row)
        if st.button("신청 내역 지우기"):
            init_data()
            st.success("Data initialized!")
        if st.button("엑셀 파일로 저장하기"):
            export_data()
