import streamlit as st
from read_data import load_person_data, get_person_list, get_picture_path
from PIL import Image
from read_pandas import read_my_csv, filter_data, make_plot, how_much_time_is_spent_in_the_zones, print_average_power_per_zone, assign_zones, make_plot_power


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

tab1, tab2, tab3= st.tabs(["ECG-Data", "HeartRate-Data", "Power-Data"])

with tab1:
    st.write("# ECG")
    
with tab2:
    df = read_my_csv()
    fig1 = make_plot(df)
    st.plotly_chart(fig1)
    

with tab3:
    df = read_my_csv()
    df = assign_zones(df)
    fig2 = make_plot_power(df)
    st.plotly_chart(fig2)



