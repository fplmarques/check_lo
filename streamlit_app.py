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
# The database consolidates the country names from CGov and regions and continents from UN m49
#
db = pd.read_csv("./localities_db.tsv", sep="\t")
db = db.drop(columns=['CAN_PROV']) # the code is intended to deal with countries not Canadian P/Ts

# Since data for Provinces were removed, I will remove duplication for Canada. These lines can be avoided if we just provide
# the initial database without Province data
db = db[db.duplicated(keep=False)]

# This is a list containing the coutry names. The code can be revised as I think we could use the column from the dataframe.
# Quick fix for now
all_countries = db['COUNTRY'].tolist()


# Function to filter the DataFrame based on user input
# I am using rapidfuzz to account for misspelling and/or names not in conformity with the current database
# There were odd behaviors in a previous version which were not tested yet
#
def filter_dataframe_by_country(input_countries, dataframe):

    # Filter the DataFrame for the matched countries
    filtered_df = dataframe[dataframe['COUNTRY'].isin(input_countries)]

    return filtered_df

# This function recover the Area Attribution based on the rules we set upt
# Has to be tested
#
def determine_area_attribution(filtered_df):
    if filtered_df.empty:
        return "No matches found.", "No affected countries."

    unique_regions = filtered_df['REGION'].dropna().unique()
    unique_continents = filtered_df['CONTINENT'].dropna().unique()

    # Determine area attribution
    if len(unique_regions) == 1:
        area_attribution = unique_regions[0]
    elif len(unique_continents) == 1:
        area_attribution = unique_continents[0]
    elif set(unique_continents) == {"Africa", "Asia", "Europe", "Oceania", "Americas"}:
        area_attribution = "Worldwide"
    else:
        area_attribution = "Multinational"


    return area_attribution


def format_affected_locations(sorted_countries):
    if len(sorted_countries) == 1:
        affected_locs = sorted_countries[0]
    elif len(sorted_countries) == 2:
        affected_locs = " and ".join(sorted_countries)
    else:
        affected_locs = ", ".join(sorted_countries[:-1]) + ", and " + sorted_countries[-1]

    return affected_locs



def main():
    # Initialize session state if necessary
    if 'selected_countries' not in st.session_state:
        st.session_state.selected_countries = []

    # Title
    st.title("Geolocation of Events/Signals:")

    # Multi-select for selecting multiple countries
    st.session_state.selected_countries = st.multiselect(
        'Select countries associated with the event/signal:', 
        all_countries, 
        default=st.session_state.selected_countries
    )

    # CSS costumization for the button

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

    # Button to process the data
    if st.button("Locate"):
        if st.session_state.selected_countries:
            # Sort the selected countries alphabetically
            sorted_countries = list(st.session_state.selected_countries)
            sorted_countries.sort()

            # Filter the DataFrame based on user input
            filtered_df = db[db['COUNTRY'].isin(sorted_countries)]

            report_as = determine_area_attribution(filtered_df)

            affected_locations = format_affected_locations(sorted_countries)

            # st.markdown(f"#### Reported Locations: {affected_locations}")

            st.markdown(
                f"""
                <span style="font-family: Arial; color: black; font-size: 26px;">Reported Locations:</span>
                <span style="font-family: Arial; color: #333333; font-size: 20px;"> {affected_locations}</span>
                """,
                unsafe_allow_html=True
            )

            # st.write(f"#### Report as: {report_as}")

            st.markdown(
                f"""
                <span style="font-family: Arial; color: black; font-size: 26px;">Report as:</span>
                <span style="font-family: Arial; color: #333333; font-size: 20px;"> {report_as}</span>
                """,
                unsafe_allow_html=True
            )


            st.markdown(f"""<span style="font-family: Arial; color: black; font-size: 26px;">Summary of Locations:</span>""", unsafe_allow_html=True)

            # st.write("#### Summary of Locations:")
            filtered_df.rename(columns={'COUNTRY': 'COUNTRY NAME'}, inplace=True) # This is for Table diplay
            # st.data_editor(filtered_df)


            st.markdown(
                """
                <style>
                .center-table {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Wrapping the table in a div for centralization
            st.markdown("<div class='center-table'>", unsafe_allow_html=True)
            st.data_editor(filtered_df)
            st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.write("No countries selected.")

if __name__ == "__main__":
    main()
