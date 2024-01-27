import streamlit as st
import malariagen_data


@st.cache_resource
def connect_ag3():
    return malariagen_data.Ag3()


ag3 = connect_ag3()


st.title('Ag3')

"""
Welcome to this app for browsing data from the MalariaGEN Vector Observatory [*Anopheles gambiae* genomic surveillance project](https://www.malariagen.net/anopheles-gambiae-genomic-surveillance-project).

Please select an option from the pages in the left sidebar to begin.
"""

st.divider()

ag3
