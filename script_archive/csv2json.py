import csv
import json

# Function to convert CSV to JSON
def csv_to_json(csv_file_path, json_file_path):
    try:
        # Open the CSV file and read it
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            # Convert rows into a list of dictionaries
            data = []
            for row in csv_reader:
                formatted_row = {key.strip(): (value.strip() if value else None) for key, value in row.items()}
                data.append(formatted_row)

        # Write the data to a JSON file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"CSV data has been successfully written to {json_file_path}")

    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
csv_file = "./UNSD_M49_official.csv"  # Replace with your input CSV file path
json_file = "./UNSD_M49_official.json"  # Replace with your desired output JSON file path
csv_to_json(csv_file, json_file)
