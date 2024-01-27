import pprint
import streamlit as st
import malariagen_data


printer = pprint.PrettyPrinter(indent=4, compact=False)


st.set_page_config(layout="wide")


@st.cache_resource
def connect_ag3():
    return malariagen_data.Ag3()


@st.cache_data
def load_sample_sets():
    ag3 = connect_ag3()
    df_ss = ag3.sample_sets()
    return df_ss


st.title('Sample sets')


df_ss = load_sample_sets()
df_sel = df_ss.copy()
df_sel.insert(0, "select", False)


edited_df = st.data_editor(
    df_sel,
    hide_index=True,
    column_config={"select": st.column_config.CheckboxColumn(required=True)},
    disabled=df_ss.columns,
    use_container_width=True,
)
selected_sets = edited_df[edited_df.select]["sample_set"].to_list()


if st.button("clear all"):
    # TODO broken
    st.write("cleared")
    df_sel["select"] = False
    edited_df["select"] = False


example_content = """
To use these sample sets in your analysis, declare a variable like this:
```
sample_sets = [
"""
for s in selected_sets:
    example_content += f"    {s!r},\n"
example_content += """]
```
"""
if selected_sets:
    st.markdown(example_content)


    """
    Here is a summary of the number of samples in these sample sets, by region, year and taxon:
    """


    ag3 = connect_ag3()
    df_ov = ag3.count_samples(sample_sets=selected_sets).reset_index()
    st.dataframe(df_ov.style, hide_index=True)


    """
    Here is a map of sampling locations:
    """


    df_samples = ag3.sample_metadata(sample_sets=selected_sets)
    df_locations = (
        df_samples
        .groupby(by=["longitude", "latitude"])
        .agg({"location": "first"})
        .reset_index()
    )
    st.map(df_locations)

else:
    """
    Select one or more sample sets to view further information.
    """