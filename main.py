import streamlit as st
from read_data import load_person_data, get_person_list, get_picture_path
from PIL import Image

person_data_dict = load_person_data()
person_list_names = get_person_list(person_data_dict)
picture_path = get_picture_path(person_data_dict)

# Eine Überschrift der ersten Ebene
st.write("# Centralized Database for Patient-Specific ECG Data")

# Eine Überschrift der zweiten Ebene
st.write("## Please select a patient")



# Eine Auswahlbox
# Auswahlbox
st.session_state.current_user = current_user = st.selectbox(
    'Patient',
    options=person_list_names, key="sbVersuchsperson")

index_current_user = person_list_names.index(current_user)

image = Image.open(picture_path[index_current_user])


st.image(image, caption=st.session_state.current_user)