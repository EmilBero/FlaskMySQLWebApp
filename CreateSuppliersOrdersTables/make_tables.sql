-- Create the suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL
);

-- Create the telephones table
CREATE TABLE IF NOT EXISTS telephones(
    supplier_id INT NOT NULL,
    telephone_number VARCHAR(20),    
    PRIMARY KEY(telephone_number),
    foreign key(supplier_id) References suppliers(id)
);

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT NOT NULL,
    order_date DATE,
    supplier_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- Create the order_parts table
CREATE TABLE IF NOT EXISTS order_parts (
    order_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, part_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (part_id) REFERENCES parts(_id)
);

