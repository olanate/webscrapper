import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(dept):
    url = requests.get(f'https://www.{dept}.ruet.ac.bd/teacher_list').text
    soup = BeautifulSoup(url, 'lxml')
    teachers = soup.find_all('tr')[1:]
    #print (teachers)
    name_en = []
    designation = []
    email = []
    phone_no = []
    depart = []

    for teacher in teachers:
        name = teacher.find_all('td')[1].text.strip()
        desig = teacher.find_all('td')[3].text.strip()
        phone = teacher.find_all('td')[6].text.strip()
        em = teacher.find_all('td')[5].text.strip()
        dept = teacher.find_all('td')[4].text.strip()

        name_en.append(name)
        designation.append(desig)
        email.append(em)
        phone_no.append(phone)
        depart.append(dept)
    
    data = pd.DataFrame({'Name': name_en, 'Designation': designation, 'Email': email, 'Phone': phone_no, 'Department': depart})
    return data

def main():
    st.title("RUET Teachers Information")
    #Department Selection
    depts = ["CSE", "EEE", "CHEM", "MATH", "PHY"]
    dept = st.sidebar.selectbox("Select Department", depts).lower()
    
    #Filter by Position using checkbox using elif
    professor = st.sidebar.checkbox("Professor")
    associate_professor = st.sidebar.checkbox("Associate Professor")
    assistant_professor = st.sidebar.checkbox("Assistant Professor")
    lecturer = st.sidebar.checkbox("Lecturer")

    position = []
    if professor:
        position.append("Professor")
    elif associate_professor:
        position.append("Associate Professor")
    elif assistant_professor:
        position.append("Assistant Professor")
    elif lecturer:
        position.append("Lecturer")

    if dept:
        data = get_data(dept)
    if position:
            data = data[data['Designation'].isin(position)]
    st.dataframe(data)

#Constructor
if __name__ == '__main__':
    main()