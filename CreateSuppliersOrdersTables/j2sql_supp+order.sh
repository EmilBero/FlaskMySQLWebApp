#!/bin/bash

# Database credentials
user="u13"
pass="54drawingBLOODchina53"
db="u13"

# Install pandas library before running python scripts
pip install pandas
echo "pandas installed"

# Convert suppliers.json and orders.json into 3 separate .csv files
python3 suppliersconvertcsv.py 
python3 ordersconvertcsv.py

# Create MySQL tables using script make_tables.sql
echo "source make_tables.sql;" | mysql -u "$user" --password="$pass" "$db"

# Convert .csv files to .tsv files 
cat suppliers.csv  | tr "," "\t" > suppliers.tsv
cat telephones.csv | tr "," "\t" > telephones.tsv
cat orders.csv  | tr "," "\t" > orders.tsv
cat part_orders.csv  | tr "," "\t" > part_orders.tsv

# Load data into MySQL tables accordingly
echo "load data local infile 'suppliers.tsv' into table suppliers" | mysql $db -u $user --password="$pass"
echo "load data local infile 'telephones.tsv' into table telephones" | mysql $db -u $user --password="$pass"
echo "load data local infile 'orders.tsv' into table orders" | mysql $db -u $user --password="$pass"
echo "load data local infile 'part_orders.tsv' into table order_parts" | mysql $db -u $user --password="$pass"

# If Bash Script Reaches this point it will print this :)
echo "Bash Script Complete."


