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

    if "selected_sets" not in st.session_state:
        st.session_state.selected_sets = []


def reset_button_on_click():
    # Trick to enable resetting the selection of sample sets. This
    # is used as part of the widget key, so forcing a recreation of
    # the widget if changed.
    st.session_state.sample_sets_reset += 1


def render_sample_sets_data_frame():
    # Grab session variables.
    reset = st.session_state.sample_sets_reset
    data = st.session_state.sample_sets_df

    # Create a data editor widget.
    sample_sets_edited_df = st.data_editor(
        data=data,
        key=f"sample_sets_data_editor_{reset}",
        hide_index=True,
        column_config={
            "selected": st.column_config.CheckboxColumn(required=True),
            "study_url": st.column_config.LinkColumn(width="small", display_text="open link"),
        },
        disabled=data.columns[1:],
    )

    # Store the edited dataframe in the session.
    st.session_state.sample_sets_edited_df = sample_sets_edited_df

    # Store a convenience variable in the session.
    selected_sets = sample_sets_edited_df[sample_sets_edited_df.selected]["sample_set"].to_list()
    st.session_state.selected_sets = selected_sets


def render_example_code():
    # Grab session variables.
    selected_sets = st.session_state.selected_sets

    # Construct markdown content, including code example.
    content = dedent("""\
        To use these sample sets in your analysis, declare a variable like this:
        ```
        sample_sets = [
    """)
    for s in selected_sets:
        content += f"    {s!r},\n"
    content += dedent("""\
        ]
        ```
    """)
    st.markdown(content)


def render_summary():
    ag3 = connect_ag3()
    selected_sets = st.session_state.selected_sets
    st.markdown("Here is a summary of the number of samples in these sample sets, by region, year and taxon:")
    df_summary = ag3.count_samples(sample_sets=selected_sets).reset_index()
    # https://discuss.streamlit.io/t/st-dataframe-controlling-the-height-threshold-for-scolling/31769/5
    height = (len(df_summary) + 1) * 35 + 3
    st.dataframe(df_summary.style, hide_index=True, height=height)


def render_map():
    ag3 = connect_ag3()
    selected_sets = st.session_state.selected_sets
    st.markdown("Here is a map of sampling locations:")
    df_samples = ag3.sample_metadata(sample_sets=selected_sets)
    df_locations = (
        df_samples
        .groupby(by=["longitude", "latitude"])
        .agg({"location": "first"})
        .reset_index()
    )
    st.map(df_locations)


def render():
    """Main rendering function."""
    st.set_page_config(layout="wide")
    init_session()
    st.title('Sample sets')
    render_sample_sets_data_frame()
    selected_sets = st.session_state.selected_sets
    if selected_sets:
        st.button("reset", key="reset_button", on_click=reset_button_on_click)
        render_example_code()
        render_summary()
        render_map()
    else:
        st.markdown("Select one or more sample sets to view further information.")


if __name__ == "__main__":
    render()
