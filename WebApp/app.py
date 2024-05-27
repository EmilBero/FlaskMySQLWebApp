from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
import locale

app = Flask(__name__)

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'u13'
DB_NAME = 'u13'
DB_PASSWORD = '54drawingBLOODchina53'

#Set locale for currency function
locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )

# App config
PORT = 20629 #provide a unique integer value instead of XXXX, e.g., PORT = 15657


def get_db_connection():
    conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
    return conn

@app.route('/')
def index():
    return render_template('index.html', name="Emil")

#show specific table
@app.route('/show-table', methods=['GET', 'POST'])
def tables():
    conn = get_db_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        #Get the submitted table name from our form
        data = []
        arr =[]
        table_name = request.form['name']
        if table_name == "suppliers_full":
            cur.execute(f"""SELECT suppliers.id, name, email, telephones.telephone_number
            FROM suppliers, telephones WHERE suppliers.id = telephones.supplier_id;""")
            data = cur.fetchall()
            arr = ["id", "name", "email", "telephone_number"]
        elif table_name == "suppliers":
            cur.execute(f"SELECT * FROM {table_name}")
            data = cur.fetchall()
            arr = ["id", "name", "email"]
        elif table_name == "parts":
            cur.execute(f"SELECT * FROM {table_name}")
            data = cur.fetchall()
            arr = ["_id","price","description"]
        elif table_name == "orders":
            cur.execute("""SELECT orders.order_date, orders.supplier_id, order_parts.part_id, order_parts.quantity
            FROM order_parts, orders WHERE order_parts.order_id = orders.id;""")
            data = cur.fetchall()
            arr =["order_date","supplier_id","part_id","quantity"]
        cur.close()
        conn.close()
        # return to frontend the data in table_name and the corresponding columns in table_name
        return render_template('show_table.html', data=data, columns=arr)
    else:
        return render_template('show_table.html', data=[], columns=[])

        
#shows expenses page and redirects user to request
@app.route("/get-expenses/", methods=['GET', 'POST'])
def get_expenses():
    if request.method =='GET':
        return render_template('annual_expenses.html', data=[])
    else:
        start = request.form["start"]
        end = request.form["end"]
        return redirect(f"/get-annual-expense/{start}/{end}")


# GET Annual Expenses for parts from start to end year
@app.route("/get-annual-expense/<string:start>/<string:end>", methods=['GET'])
def total_expense(start, end):
    conn = get_db_connection()
    cur = conn.cursor()
    #SQL query to get total expenses for each year
    cur.execute(f"""SELECT YEAR(order_date) as year,  sum(price*quantity) FROM
    order_parts, parts, orders WHERE
    order_parts.part_id = parts._id AND orders.id = order_parts.order_id AND
    YEAR(order_date)>={start} AND YEAR(order_date)<={end} GROUP BY YEAR(order_date);""")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('annual_expenses.html', data=data, currency=locale.currency)

#Budget Projection
@app.route("/budget-projection", methods=['GET', 'POST'])
def budget_projection():
    if request.method == "GET":
        return render_template('budget_projection.html', data=[])
    else:
        #Get number of years and inflation rate
        years = int(request.form["numYears"])
        rate = float(request.form["rate"])
        arr = []
        conn = get_db_connection()
        cur = conn.cursor()
        #SQL query to get the recent expense
        cur.execute("""SELECT YEAR(order_date) as year, sum(price*quantity)
        FROM order_parts, parts, orders
        WHERE order_parts.part_id = parts._id AND orders.id = order_parts.order_id AND YEAR(order_date)=2022
        GROUP BY YEAR(order_date);""")
        data = cur.fetchall()
        recent_year = data[0][0]
        recent_expense = data[0][1]
        total_rate = (100+rate)/100
        #Add tuple containg new year and projected expenses for the year
        for i in range (1, years+1):
            arr.append((recent_year+i, float("{:.2f}".format((recent_expense)*(total_rate)**(i)))))
        cur.close()
        conn.close()
        return render_template('budget_projection.html', data=arr, currency=locale.currency)


@app.route("/add-supplier", methods=['GET', 'POST'])
def add_supplier():
    if request.method == "GET":
        return render_template('add_supplier.html', data=[], error=None)
    else:
        _id = request.form["id"]
        name = request.form["name"]
        email = request.form["email"]
        numbers = request.form["numbers"].split(",")
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if supplier exists with _id
        cur.execute(f"SELECT * FROM suppliers WHERE id = {_id}")
        existing_supplier = cur.fetchone()
        
        if existing_supplier:
            # Supplier with the same ID already exists, return with error message
            error = "Supplier already exists. Please try using a different Supplier ID."
            return render_template('add_supplier.html', data=[], error=error)
        
        # Check for duplicate telephone numbers
        duplicate_numbers = []
        for number in numbers:
            cur.execute(f"SELECT * FROM telephones WHERE telephone_number = '{number}'")
            existing_number = cur.fetchone()
            if existing_number:
                duplicate_numbers.append(number)
        
        if duplicate_numbers:
            # At least one telephone number is already in use, return with error message
            error = f"The telephone number(s): {', '.join(duplicate_numbers)} is already in use. Please use different ones."
            return render_template('add_supplier.html', data=[], error=error)
        
        # Insert into supplier relation
        cur.execute(f"INSERT INTO suppliers(id, name, email) VALUES ({_id}, '{name}', '{email}')")
        
        # Insert numbers into telephone relation
        for number in numbers:
            cur.execute(f"INSERT INTO telephones(supplier_id, telephone_number) VALUES ({_id}, '{number}')")
        
        conn.commit()
        
        # Retrieve the newly inserted supplier details
        cur.execute(f"""SELECT suppliers.id, name, email, telephones.telephone_number
                        FROM suppliers, telephones
                        WHERE suppliers.id = telephones.supplier_id AND suppliers.id={_id} ;""")
        data = cur.fetchall()
        
        arr = ["id", "name", "email", "telephone_numbers"]
        cur.close()
        conn.close()
        return render_template('add_supplier.html', data=data, columns=arr, error=None)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
