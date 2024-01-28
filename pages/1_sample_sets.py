from textwrap import dedent
import streamlit as st
import malariagen_data  # type: ignore


@st.cache_resource
def connect_ag3():
    return malariagen_data.Ag3()


@st.cache_data
def load_sample_sets():
    ag3 = connect_ag3()
    df_ss = ag3.sample_sets()
    return df_ss


def init_session():

    if "sample_sets_reset" not in st.session_state:
        st.session_state.sample_sets_reset = 0

    if "sample_sets_df" not in st.session_state:
        sample_sets_df = load_sample_sets()
        sample_sets_df.insert(0, "selected", False)
        st.session_state.sample_sets_df = sample_sets_df


def reset_button_on_click():
    st.session_state.sample_sets_reset += 1


def render_sample_sets_data_frame():
    reset = st.session_state.sample_sets_reset
    data = st.session_state.sample_sets_df
    st.session_state.sample_sets_edited_df = st.data_editor(
        data=data,
        key=f"sample_sets_data_editor_{reset}",
        hide_index=True,
        column_config={
            "selected": st.column_config.CheckboxColumn(required=True),
        },
        disabled=data.columns[1:],
        use_container_width=True,
    )
    st.button("reset", key="reset_button", on_click=reset_button_on_click)


def render_example_code():
    data = st.session_state.sample_sets_edited_df
    selected_sets = data[data.selected]["sample_set"].to_list()
    example_content = dedent("""\
        To use these sample sets in your analysis, declare a variable like this:
        ```
        sample_sets = [
    """)
    for s in selected_sets:
        example_content += f"    {s!r},\n"
    example_content += dedent("""\
        ]
        ```
    """)
    if selected_sets:
        st.markdown(example_content)



def render():
    st.set_page_config(layout="wide")
    init_session()
    st.title('Sample sets')
    render_sample_sets_data_frame()
    render_example_code()


if __name__ == "__main__":
    render()


#     """
#     Here is a summary of the number of samples in these sample sets, by region, year and taxon:
#     """


#     ag3 = connect_ag3()
#     df_ov = ag3.count_samples(sample_sets=selected_sets).reset_index()
#     st.dataframe(df_ov.style, hide_index=True)


#     """
#     Here is a map of sampling locations:
#     """


#     df_samples = ag3.sample_metadata(sample_sets=selected_sets)
#     df_locations = (
#         df_samples
#         .groupby(by=["longitude", "latitude"])
#         .agg({"location": "first"})
#         .reset_index()
#     )
#     st.map(df_locations)

# else:
#     """
#     Select one or more sample sets to view further information.
#     """