import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
 
def get_data(which_dept):
    url = requests.get(f'https://www.{which_dept}.ruet.ac.bd/teacher_list').text
    soup = BeautifulSoup(url, 'lxml')
    teachers = soup.find_all('tr')[1:]
    names = []
    designations = []
    phones = []
    emails = []
    depts = []
    for teacher in teachers:
        td = teacher.find_all('td')
        name = td[1].text.strip()
        names.append(name)
        designation = td[3].text.strip()
        designations.append(designation)
        phone = td[6].text.strip()
        phones.append(phone)
        email = td[5].text.strip()
        emails.append(email)
        dept = td[4].text.strip()
        depts.append(dept)
    data = pd.DataFrame({'Name': names, 'Designation': designations, 'Phone': phones,
                         'Email': emails, 'Department': depts})
    return data
 
def main():
    st.title("RUET teachers information")
    depts = ['EEE', 'CSE', 'CHEM', 'MATH', 'PHY', 'CHEM']
    dept = st.sidebar.selectbox('Select Department', depts).lower()
    prof = st.sidebar.checkbox('Professor', value=True)
    assistant_prof = st.sidebar.checkbox('Assistant Professor', value=True)
    associate_prof = st.sidebar.checkbox('Associate Professor', value=True)
    lecturer = st.sidebar.checkbox('Lecturer', value=True)
 
    if dept:
        data = get_data(dept)
        cp = data.copy()
 
        if (prof is False):
            cp = cp[cp['Designation'] != 'Professor']
 
        if (assistant_prof is False):
            cp = cp[cp['Designation'] != 'Assistant Professor']
 
        if (associate_prof is False):
            cp = cp[cp['Designation'] != 'Associate Professor']
 
        if (lecturer is False):
            cp = cp[cp['Designation'] != 'Lecturer']
 
        st.dataframe(cp)
 
main()