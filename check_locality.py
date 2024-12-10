
import json

def find_common_regions(file_path, countries):
    """
    Load the M49 JSON file and return the common region, sub-region, and intermediate region names
    for the specified list of countries.
    
    :param file_path: Path to the M49 JSON file.
    :param countries: List of country or area names.
    :return: Dictionary with "Intermediate Region Name", "Sub-region Name", and "Region Name".
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Filter entries corresponding to the provided countries
    filtered_data = [entry for entry in data if entry["Country or Area"] in countries]
    
    if not filtered_data:
        return {"Intermediate Region Name": "Worldwide", 
                "Sub-region Name": "Worldwide", 
                "Region Name": "Worldwide"}
    
    # Extract region names
    intermediate_regions = {entry["Intermediate Region Name"] for entry in filtered_data}
    sub_regions = {entry["Sub-region Name"] for entry in filtered_data}
    regions = {entry["Region Name"] for entry in filtered_data}
    
    # Determine commonality
    intermediate_region = intermediate_regions.pop() if len(intermediate_regions) == 1 else "Worldwide"
    sub_region = sub_regions.pop() if len(sub_regions) == 1 else "Worldwide"
    region = regions.pop() if len(regions) == 1 else "Worldwide"
    
    return {
        "Intermediate Region Name": intermediate_region,
        "Sub-region Name": sub_region,
        "Region Name": region
    }

# Example usage
file_path = '2022-09-24__JSON_UNSD_M49.json'
countries = ["Burkina Faso", "Cabo Verde"]
result = find_common_regions(file_path, countries)
print(result)
