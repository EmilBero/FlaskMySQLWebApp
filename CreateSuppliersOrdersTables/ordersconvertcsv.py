import json
import pandas as pd

# Specify the path to your JSON file
file_path_orders = 'orders_4000.json'

# Read the JSON data
with open(file_path_orders, 'r') as file:
    orders_data = file.readlines()

# Normalize the data to create orders and part_orders DataFrames
orders_info = []
part_orders_info = []

# Extracting order data and part_order data
for i, line in enumerate(orders_data):
    order = json.loads(line)
    orders_info.append({
        'id': i + 1,  # Generating a unique order ID as it's not provided in the JSON
        'order_date': order['when'],
        'supplier_id': order['supp_id']
    })
    for item in order['items']:
        part_orders_info.append({
            'order_id': i + 1,  # Using the generated order ID
            'part_id': item['part_id'],
            'quantity': item['qty']
        })

orders_df = pd.DataFrame(orders_info)
part_orders_df = pd.DataFrame(part_orders_info)

# Save the DataFrames to CSV files
orders_csv_path = 'orders.csv'
part_orders_csv_path = 'part_orders.csv'
orders_df.to_csv(orders_csv_path, index=False, header=False)
part_orders_df.to_csv(part_orders_csv_path, index=False, header=False)

