import pandas as pd
import streamlit as st


# Inject custom CSS for styling
st.markdown(
    """
    <style>
    /* Change the font color of selected options in the multiselect dropdown */
    .css-163ttbj.e16nr0p33:focus, .css-163ttbj.e16nr0p33 {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the CSV file into a DataFrame
db = pd.read_csv("./localities_db.tsv", sep="\t")
db = db.drop(columns=['CAN_PROV'])  # the code is intended to deal with countries not Canadian P/Ts

# Remove duplication for Canada
db = db.drop_duplicates()

# This is a list containing the country names
all_countries = db['COUNTRY'].tolist()


def determine_area_attribution(filtered_df, selected_countries):
    if len(selected_countries) == 1:
        # Use the single country name as the report
        return selected_countries[0]
    
    unique_regions = filtered_df['REGION'].dropna().unique()
    unique_continents = filtered_df['CONTINENT'].dropna().unique()

    # Determine area attribution
    if len(unique_regions) == 1:
        return unique_regions[0]
    elif len(unique_continents) == 1:
        return unique_continents[0]
    elif set(unique_continents) == {"Africa", "Asia", "Europe", "Oceania", "Americas"}:
        return "Worldwide"
    else:
        return "Multiregional"


def format_affected_locations(sorted_countries):
    if len(sorted_countries) == 1:
        return sorted_countries[0]
    elif len(sorted_countries) == 2:
        return " and ".join(sorted_countries)
    else:
        return ", ".join(sorted_countries[:-1]) + ", and " + sorted_countries[-1]


def main():
    if 'selected_countries' not in st.session_state:
        st.session_state.selected_countries = []

    st.title("Geolocation of Events/Signals:")

    selected_countries = st.multiselect(
        'Select areas associated with the event/signal:',
        all_countries,
        format_func=lambda x: x if x else "Unknown",
    )

    st.session_state.selected_countries = selected_countries

    if selected_countries:
        sorted_countries = sorted(selected_countries)
        filtered_df = db[db['COUNTRY'].isin(sorted_countries)]
        st.markdown(
            "<span style='font-family: Arial; color: black; font-size: 26px;'>Selected areas:</span>",
            unsafe_allow_html=True,
        )
        filtered_df.rename(columns={'COUNTRY': 'COUNTRY NAME'}, inplace=True)
        st.data_editor(filtered_df)

    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #2092e9;
            color: white;
            padding: 10px 20px;
            font-size: 20px;
            border-radius: 5px;
            border: outset;
            cursor: pointer;
        }
        div.stButton > button:hover {
            background-color: #2092e9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Summarize"):
        if selected_countries:
            sorted_countries = sorted(selected_countries)
            filtered_df = db[db['COUNTRY'].isin(sorted_countries)]
            report_as = determine_area_attribution(filtered_df, selected_countries)
            affected_locations = format_affected_locations(sorted_countries)

            st.markdown(
                f"""
                <span style="font-family: Arial; color: black; font-size: 26px;">Affected Locations:</span>
                <span style="font-family: Arial; color: #333333; font-size: 20px;"> {affected_locations}</span>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <span style="font-family: Arial; color: black; font-size: 26px;">Report as:</span>
                <span style="font-family: Arial; color: #333333; font-size: 20px;"> {report_as}</span>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.write("No countries selected.")

if __name__ == "__main__":
    main()
