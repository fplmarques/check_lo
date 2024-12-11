
# LYBRARIES
import json

from rapidfuzz import process
from coutry_or_areas import M49_countries_or_areas



def check_M49_proper_names(input_localities, M49_countries_or_areas):
    revised_localities = []

    for locality in input_localities:

        # Find the closest match
        closest_match = process.extractOne(locality, M49_countries_or_areas)

        revised_localities.append(closest_match[0])

    return revised_localities


def find_common_regions(json_file, countries):
    # Load JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter data for selected countries
    filtered_data = [entry for entry in data if entry['Country or Area'] in countries]
    print_filetered(filtered_data)
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
        return "No common region found: Multinational"

def  print_filetered(filtered_list):
    for country in filtered_list:
        print(country['Region Name'], country['Sub-region Name'], country['Intermediate Region Name'], country['Country or Area'])

def main():
    json_file = '2022-09-24__JSON_UNSD_M49.json'
    countries = input("Enter countries separated by commas: ")
    # countries = 'Estonia, Finland, France, Germany, Ireland, Netherlands, United Kingdom'
    # print(countries)
    countries = countries.split(',')
    countries = [country.strip() for country in countries]
    print(f"Input coun tries: {countries}")
    countries = check_M49_proper_names(countries, M49_countries_or_areas)
    print(f"Revised names: {countries}")
    common_region = find_common_regions(json_file, countries)
    print(f"Common region: {common_region}")


if __name__ == "__main__":
    main()
