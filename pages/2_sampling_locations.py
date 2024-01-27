import streamlit as st
import malariagen_data


@st.cache_resource
def connect_ag3():
    return malariagen_data.Ag3()


@st.cache_data
def load_locations_data():
    ag3 = connect_ag3()
    df_samples = ag3.sample_metadata()
    df_locations = (
        df_samples
        .groupby(["longitude", "latitude"])
        .agg({"location": "first"})
        .rename(columns={"location": "info"})
        .reset_index()
    )

    return df_locations


st.title('Ag3 - Map of sampling locations')


df_locations = load_locations_data()
st.map(df_locations)