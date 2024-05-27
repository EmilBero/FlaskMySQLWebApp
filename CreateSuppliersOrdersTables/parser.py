import pymysql
import json

# Database connection details
host = 'dbcourse.cs.smu.ca'
user = 'u13'
password = '54drawingBLOODchina53'
database = 'u13'

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# Read and parse the JSON file containing orders
with open('orders_4000.json') as file:
    orders = file.readlines()

# Insert orders into the orders table
for order_json in orders:
    order_data = json.loads(order_json)
    
    order_date = order_data['when']
    supplier_id = order_data['supp_id']
    
    # Insert the order into the orders table
    cursor.execute("INSERT INTO orders (order_date, supplier_id) VALUES (%s, %s)", (order_date, supplier_id))
    
    # Get the ID of the last inserted order
    order_id = cursor.lastrowid
    
    # Insert the order parts into the order_parts table
    for part in order_data['items']:
        part_id = part['part_id']
        quantity = part['qty']
        cursor.execute("INSERT INTO order_parts (order_id, part_id, quantity) VALUES (%s, %s, %s)", (order_id, part_id, quantity))

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Data import completed.")

