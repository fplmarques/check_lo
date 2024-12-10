import json

def find_common_regions(file_path, countries):
    """
    Load the M49 JSON file and return the common region, sub-region, and intermediate region names
    for the specified list of countries. Returns the highest common level for the given countries.
    
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
    
    # Extract unique region levels
    intermediate_regions = {entry["Intermediate Region Name"] for entry in filtered_data if entry["Intermediate Region Name"]}
    sub_regions = {entry["Sub-region Name"] for entry in filtered_data if entry["Sub-region Name"]}
    regions = {entry["Region Name"] for entry in filtered_data if entry["Region Name"]}
    
    # Check the highest commonality level
    if len(intermediate_regions) == 1:
        return {
            "Intermediate Region Name": intermediate_regions.pop(),
            "Sub-region Name": sub_regions.pop() if len(sub_regions) == 1 else "Worldwide",
            "Region Name": regions.pop() if len(regions) == 1 else "Worldwide"
        }
    elif len(sub_regions) == 1:
        return {
            "Intermediate Region Name": "Worldwide",
            "Sub-region Name": sub_regions.pop(),
            "Region Name": regions.pop() if len(regions) == 1 else "Worldwide"
        }
    elif len(regions) == 1:
        return {
            "Intermediate Region Name": "Worldwide",
            "Sub-region Name": "Worldwide",
            "Region Name": regions.pop()
        }
    else:
        return {"Intermediate Region Name": "Worldwide", 
                "Sub-region Name": "Worldwide", 
                "Region Name": "Worldwide"}

# Example usage
file_path = '2022-09-24__JSON_UNSD_M49.json'
countries = ["Burkina Faso", "Cabo Verde"]
result = find_common_regions(file_path, countries)
print(result)
