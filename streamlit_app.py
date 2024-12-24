import pandas as pd
from rapidfuzz import process
import streamlit as st

# Load the CSV file into a DataFrame
# The database consolidates the country names from CGov and regions and continents from UN m49
#
db = pd.read_csv("./localities_db.tsv", sep="\t")
db = db.drop(columns=['CAN_PROV']) # the code is intended to deal with countries not Canadian P/Ts

# Function to filter the DataFrame based on user input
# I am using rapidfuzz to account for misspelling and/or names not in conformity with the current database
# There were odd behaviors in a previous version which were not tested yet
#
def filter_dataframe_by_country(input_countries, dataframe):
    # Split the input string into a list of countries
    input_country_list = [country.strip() for country in input_countries.split(",")]

    # Get all unique countries in the dataframe
    all_countries = dataframe['COUNTRY'].dropna().unique()

    # Map user input countries to the closest matches in the DataFrame
    matched_countries = []
    for country in input_country_list:
        match_result = process.extractOne(country, all_countries)
        matched_countries.append(match_result[0])

    # Filter the DataFrame for the matched countries
    filtered_df = dataframe[dataframe['COUNTRY'].isin(matched_countries)]

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

    # Affected countries
    affected_countries = ", ".join(filtered_df['COUNTRY'].unique())

    return area_attribution, affected_countries

	
# The main function to run in Streamlit
def main():
    st.title("Check Attribution of Areas:")

    # User input for countries
    user_input = st.text_input("Enter a list of countries (separated by commas):", "")

    if user_input:
        # Filter the DataFrame based on user input
        filtered_df = filter_dataframe_by_country(user_input, db)

        # Display the filtered DataFrame
        if filtered_df.empty:
            st.write("No matches found.")
        else:
            st.write("### Filtered Results")
            st.dataframe(filtered_df)

        # Determine and display area attribution and affected countries
        area_attribution, affected_countries = determine_area_attribution(filtered_df)
        st.write("### Area Attribution")
        st.write(area_attribution)
        st.write("### Affected Countries")
        st.write(affected_countries)

if __name__ == "__main__":
    main()
