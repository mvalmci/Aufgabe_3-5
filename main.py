import streamlit as st
from read_data import load_person_data, get_person_list, get_picture_path
from PIL import Image
from read_pandas import read_my_csv, make_plot, how_much_time_is_spent_in_the_zones, assign_zones, make_plot_power, average_power_per_zone

person_data_dict = load_person_data()
person_list_names = get_person_list(person_data_dict)
picture_path = get_picture_path(person_data_dict)

#Streamlit
st.set_page_config(
    page_title="Patient ECG Data",
    page_icon=":heart:",
    layout="wide",
    initial_sidebar_state="expanded"
)
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

tab1, tab2= st.tabs(["HeartRate-Data", "Power-Data"])

with tab1:
    df = read_my_csv()
    input_max_hr = st.number_input(
        "Maximale Herzfrequenz (bpm)",
        min_value=100,
        max_value=250,
        value=180,
        step=1,
        help="Die maximale Herzfrequenz wird für die Zonenberechnung benötigt."
    )
    df = assign_zones(df, max_hr=input_max_hr)
    fig1 = make_plot(df)
    st.plotly_chart(fig1)

    zone_times = how_much_time_is_spent_in_the_zones(df)

    a, b, c, d, e = st.columns(5)

    a.metric("Zone 1 in min.", f"{zone_times['zone1']:.1f}", "+", border=True)
    b.metric("Zone 2 in min.", f"{zone_times['zone2']:.1f}", "+", border=True)
    c.metric("Zone 3 in min.", f"{zone_times['zone3']:.1f}", "+", border=True)
    d.metric("Zone 4 in min.", f"{zone_times['zone4']:.1f}", "+", border=True)
    e.metric("Zone 5 in min.", f"{zone_times['zone5']:.1f}", "+", border=True)
    

with tab2:
    df = read_my_csv()
    df = assign_zones(df, max_hr=190)
    fig2 = make_plot_power(df)
    st.plotly_chart(fig2)

    zone_avg_power = average_power_per_zone(df)

    f, g, h, j, k = st.columns(5)

    f.metric("Ø Power Zone 1", f"{zone_avg_power['zone1']:.1f}", "+", border=True)
    g.metric("Ø Power Zone 2", f"{zone_avg_power['zone2']:.1f}", "+", border=True)
    h.metric("Ø Power Zone 3", f"{zone_avg_power['zone3']:.1f}", "+", border=True)
    j.metric("Ø Power Zone 4", f"{zone_avg_power['zone4']:.1f}", "+", border=True)
    k.metric("Ø Power Zone 5", f"{zone_avg_power['zone5']:.1f}", "+", border=True)
