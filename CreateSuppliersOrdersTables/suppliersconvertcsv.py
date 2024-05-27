import json
import pandas as pd

# Load the JSON data from a file (replace 'your_file_path.json' with your actual file path)
with open('suppliers_100.json', 'r') as file:
    suppliers_data = json.load(file)

# Extract suppliers information
suppliers_info = [{
    'id': supplier['_id'],
    'name': supplier['name'],
    'email': supplier['email'],
    'telephone': supplier['tel']
} for supplier in suppliers_data]

# Create DataFrame for suppliers
suppliers_df = pd.DataFrame(suppliers_info)

# Save the DataFrame to a CSV file (specify your desired file path)
suppliers_csv_path = 'suppliers.csv'
suppliers_df.to_csv(suppliers_csv_path, index=False, header=False)


import json
import pandas as pd

# Load the JSON data from a file (replace 'your_file_path.json' with your actual file path)
with open('suppliers_100.json', 'r') as file:
    suppliers_data = json.load(file)

# Extract suppliers information
suppliers_info = [{
    'id': supplier['_id'],
    'name': supplier['name'],
    'email': supplier['email']
} for supplier in suppliers_data]

# Create DataFrame for suppliers
suppliers_df = pd.DataFrame(suppliers_info)

# Extract telephones information
telephones_info = []
for supplier in suppliers_data:
    for tel in supplier['tel']:
        telephones_info.append({
            'supplier_id': supplier['_id'],
            'telephones': tel['number']
        })

# Create DataFrame for telephones
telephones_df = pd.DataFrame(telephones_info)

# Save the DataFrames to CSV files (specify your desired file paths)
suppliers_csv_path = 'suppliers.csv'
telephones_csv_path = 'telephones.csv'
suppliers_df.to_csv(suppliers_csv_path, index=False, header=False)
telephones_df.to_csv(telephones_csv_path, index=False, header=False)
