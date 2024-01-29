from textwrap import dedent
import streamlit as st
import malariagen_data  # type: ignore


class Keys:
    SAMPLES_DF = "samples_df"
    MULTISELECT_COUNTRIES = "multiselect_countries"
    MULTISELECT_TAXA = "multiselect_taxa"
    MULTISELECT_YEARS = "multiselect_years"


@st.cache_resource
def connect_ag3():
    return malariagen_data.Ag3()


@st.cache_data
def load_sample_metadata():
    ag3 = connect_ag3()
    samples_df = ag3.sample_metadata()
    return samples_df


def init_session():
    if Keys.SAMPLES_DF not in st.session_state:
        st.session_state[Keys.SAMPLES_DF] = load_sample_metadata()
    if Keys.MULTISELECT_COUNTRIES not in st.session_state:
        st.session_state[Keys.MULTISELECT_COUNTRIES] = []
    if Keys.MULTISELECT_TAXA not in st.session_state:
        st.session_state[Keys.MULTISELECT_TAXA] = []
    if Keys.MULTISELECT_YEARS not in st.session_state:
        st.session_state[Keys.MULTISELECT_YEARS] = []


def render_query():
    query_components = []
    countries = st.session_state[Keys.MULTISELECT_COUNTRIES]
    if countries:
        q = f"country in {countries}"
        query_components.append(q)
    taxa = st.session_state[Keys.MULTISELECT_TAXA]
    if taxa:
        q = f"taxon in {taxa}"
        query_components.append(q)
    years = sorted(st.session_state[Keys.MULTISELECT_YEARS])
    if years:
        q = f"year in {years}"
        query_components.append(q)

    sample_query = None
    if len(query_components) == 1:
        sample_query = query_components[0]
        content = dedent(f"""
            ```
            sample_query = {sample_query!r}
            ```
        """)
        st.markdown(content)

    elif len(query_components) > 1:
        sample_query = " and ".join(query_components)
        content = dedent("""\
            ```
            sample_query = (
        """)
        for q in query_components[:-1]:
            content += f"    {q + ' and '!r}\n"
        content += f"    {query_components[-1]!r}\n"
        content += dedent("""\
            )
            ```
        """)
        st.markdown(content)

    else:
        content = dedent("""
            ```
            Please select options below to begin building a query...
            ```
        """)
        st.markdown(content)

    samples_df = st.session_state[Keys.SAMPLES_DF]
    if sample_query:
        results = samples_df.query(sample_query)
    else:
        results = samples_df
    st.markdown(f"No. samples: {len(results):,}")


def render_country():
    samples_df = st.session_state[Keys.SAMPLES_DF]
    countries = sorted(samples_df["country"].unique().tolist())
    # st.markdown("## Countries")
    st.multiselect(
        label="Countries:",
        options=countries,
        key=Keys.MULTISELECT_COUNTRIES,
    )


def render_taxon():
    samples_df = st.session_state[Keys.SAMPLES_DF]
    taxa = sorted(samples_df["taxon"].unique().tolist())
    # st.markdown("## Taxa")
    st.multiselect(
        label="Taxa (species):",
        options=taxa,
        key=Keys.MULTISELECT_TAXA,
    )


def render_year():
    samples_df = st.session_state[Keys.SAMPLES_DF]
    years = sorted(samples_df["year"].unique().tolist())
    years = [y for y in years if y > 0]
    # st.markdown("## Years")
    st.multiselect(
        label="Years:",
        options=years,
        key=Keys.MULTISELECT_YEARS,
    )


def render():
    """Main rendering function."""
    st.set_page_config(layout="wide")
    init_session()
    st.title('Sample query builder')
    render_query()
    st.divider()
    render_country()
    render_taxon()
    render_year()


if __name__ == "__main__":
    render()
