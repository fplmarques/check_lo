import json

def find_common_regions(json_file, countries):
    # Load JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter data for selected countries
    filtered_data = [entry for entry in data if entry['Country or Area'] in countries]

    # If any country is missing, return None
    if len(filtered_data) != len(countries):
        return None

    # Extract unique values for each region level
    intermediate_regions = {entry['Intermediate Region Name'] for entry in filtered_data if entry['Intermediate Region Name']}
    sub_regions = {entry['Sub-region Name'] for entry in filtered_data if entry['Sub-region Name']}
    regions = {entry['Region Name'] for entry in filtered_data if entry['Region Name']}

    # Check commonality
    if len(intermediate_regions) == 1:
        return list(intermediate_regions)[0]
    elif len(sub_regions) == 1:
        return list(sub_regions)[0]
    elif len(regions) == 1:
        return list(regions)[0]
    else:
        return "No common region found"

# Example usage
json_file = '2022-09-24__JSON_UNSD_M49.json'
countries = ["Burkina Faso", "Cabo Verde"]
common_region = find_common_regions(json_file, countries)
print(f"Common region: {common_region}")
