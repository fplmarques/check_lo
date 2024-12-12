import json
import streamlit as st
from rapidfuzz import process
from country_or_areas import M49_countries_or_areas, can_gov_countries_or_areas

def check_proper_names(input_localities, countries_or_areas):
    revised_localities = []
    
    for locality in input_localities:
        # Find the closest match
        closest_match = process.extractOne(locality, countries_or_areas)
        revised_localities.append(closest_match[0])

    return revised_localities

def find_common_regions(json_file, countries):
    # Load JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter data for selected countries
    filtered_data = [entry for entry in data if entry['Country or Area'] in countries]
    

    # Display filtered data as a table
    if filtered_data:
        st.write("**UNSD M49 labels:**")
        # Create a table-friendly structure
        table_data = [
            {
                "Region Name": country['Region Name'],
                "Sub-region Name": country['Sub-region Name'],
                "Intermediate Region Name": country['Intermediate Region Name'],
                "Country or Area": country['Country or Area']
            }
            for country in filtered_data
        ]
        # Display the table
        st.table(table_data)
    else:
        st.write("No data available for the selected countries.")

    
    # If any country is missing, return None
    if len(filtered_data) != len(countries):
        return "Check country names"

    # Extract unique values for each region level
    intermediate_regions = {entry['Intermediate Region Name'] if entry['Intermediate Region Name'] else 'no_attribute' for entry in filtered_data}
    sub_regions = {entry['Sub-region Name'] if entry['Sub-region Name'] else 'no_attribute' for entry in filtered_data}
    regions = {entry['Region Name'] if entry['Region Name'] else 'no_attribute' for entry in filtered_data}

    # Check commonality
    if len(intermediate_regions) == 1 and list(intermediate_regions)[0] != 'no_attribute':
        return list(intermediate_regions)[0]
    elif len(sub_regions) == 1 and list(sub_regions)[0] != 'no_attribute':
        return list(sub_regions)[0]
    elif len(regions) == 1 and list(regions)[0] != 'no_attribute':
        return list(regions)[0]
    else:
        return "Multinational"

def main():
    st.title("M49 Country or Area Region Checker")

    # JSON file generated from official CSV file
    json_file = 'UNSD_M49_official.json'

    # Input countries
    input_countries = st.text_area("Enter countries separated by commas:")
    if not input_countries:
        st.warning("Please enter at least one country.")
        return

    # Handling substitutions for special cases:
    input_countries = input_countries.replace("North Korea", "Democratic People's Republic of Korea")
    input_countries = input_countries.replace("South Korea", "Republic of Korea")
    input_countries = input_countries.replace("Macao", "Macao Special Administrative Region")
    input_countries = input_countries.replace("West Bank and Gaza", "State of Palestine")
    input_countries = input_countries.replace("Gaza", "State of Palestine")
    input_countries = input_countries.replace("West Bank", "State of Palestine")

    # Building lis and removing leading and training spaces
    input_countries = [country.strip() for country in input_countries.split(',')]

    # Validate and revise country names
    countries = check_proper_names(input_countries, M49_countries_or_areas)
    # This will remove duplicates from M49 country assignment (comma related)
    countries = list(set(countries))
    
    affected_areas = check_proper_names(input_countries, can_gov_countries_or_areas)
    # Removing duplicates (comma related)
    affected_areas = list(set(affected_areas))
    
    # Transforming affected araes in string for report
    if len(affected_areas) == 1:
        affected_areas = affected_areas[0]
    else:
        affected_areas = ", ".join(affected_areas[:-1]) + ", and " + affected_areas[-1]
    
    st.write("**Revised country names (UNSD M49):**", countries)

    # Find common region
    common_region = find_common_regions(json_file, countries)
    st.write("**Common (sub-)Region:**", common_region)
    st.write("**Affected areas:**", affected_areas)

if __name__ == "__main__":
    main()
