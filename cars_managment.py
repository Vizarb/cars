import sqlite3
from enum import Enum
import os

# Connect to the SQLite database
con = sqlite3.connect("cars.db")
cur = con.cursor()  # In order to execute SQL statements and fetch results from SQL queries, we will need to use a database cursor.

def alter_sseerrveerrss(cur):
    cur.execute("""ALTER TABLE cars
ADD FOREIGN KEY (CustomersId) REFERENCES Customers (CustomersId) ;""")


def create_tables(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        CustomersId INTEGER PRIMARY KEY AUTOINCREMENT,
        Fname TEXT,
        Sname TEXT,
        Email VARCHAR(255)
    );""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS cars (
        CarId INTEGER PRIMARY KEY AUTOINCREMENT,
        Brand TEXT,
        Year INTEGER,
        Color TEXT,
        CustomerId INTEGER,
        FOREIGN KEY (CustomerId) REFERENCES customers (CustomersId)
    );""")

def add_customers():  # Adds a new car to the database
    fname = input("Enter fname: ").strip()
    sname = input("Enter sname: ").strip()
    email = input("Enter email: ").strip()
    data = [fname, sname, email]
    cur.execute("INSERT INTO customers (Fname, Sname, Email) VALUES (?, ?, ?)", data)
    con.commit()
    
    print("customer added successfully!")
    add_cars()



class Menues_option(Enum):  # Defines Enum for menu options
    SHOW = 1
    ADD = 2
    DELETE = 3
    EDIT = 4
    SEARCH_CAR = 5
    SEARCH_Customers = 6
    EXIT = 999

def display_menu():  # Displays the menu
    for option in Menues_option:
        print(f"{option.value}. {option.name}")

def show_all_cars():  # Shows all cars from the database
    res = cur.execute("SELECT * FROM cars")
    rows = res.fetchall()
    for row in rows:
        print(row)




def add_cars():  # Adds a new car to the database
    # Retrieve the most recently added customer's ID
    cur.execute("SELECT CustomersId FROM customers ORDER BY CustomersId DESC LIMIT 1")
    last_customer_id = cur.fetchone()
    
    if last_customer_id:
        brand = input("Enter brand: ").strip()
        year = input("Enter Year: ").strip()
        color = input("Enter Color: ").strip()
        data = [brand, int(year), color, last_customer_id[0]]
        
        cur.execute("INSERT INTO cars (Brand, Year, Color, CustomerId) VALUES (?, ?, ?, ?)", data)
        con.commit()
        print("Car added successfully!")
    else:
        print("No customer found. Please add a customer first.")


def delete_car():  # Deletes a car from the database based on ID
    car_id = input("Enter ID: ").strip()
    cur.execute("DELETE FROM cars WHERE Id = ?", (car_id,))
    con.commit()
    print("Car deleted successfully!")

def update_cars():  # Updates car details based on ID
    brand = input("Enter brand: ").strip()
    year = int(input("Enter Year: "))
    color = input("Enter Color: ").strip()
    car_id = int(input("Enter car ID: "))
    cur.execute("UPDATE cars SET Brand = ?, Year = ?, Color = ? WHERE Id = ?", (brand, year, color, car_id))
    con.commit()
    print("Car updated successfully!")

def search_car_brand():  # Searches for cars by brand name
    brand = input("Enter car brand name to search: ").strip()
    res = cur.execute("SELECT * FROM cars WHERE Brand = ?", (brand,))
    rows = res.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No cars found with that brand name.")

def search_Customers():  # Searches for cars by brand name
    fname = input("Enter first name to search: ").strip()
    email = input("Enter email to search: ").strip()
    res = cur.execute("""
    SELECT customers.*, cars.Brand, cars.Year, cars.Color
    FROM customers
    INNER JOIN cars ON customers.CustomersId = cars.CustomerId
    WHERE customers.Fname = ? AND customers.Email = ?
    """, (fname,email))
    rows = res.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No Customers found with that name.")


def menu():  # Main menu function
    while True:
        input("Click Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        display_menu()
        try:
            user_input = int(input('Please select your choice: '))
            selected_option = Menues_option(user_input)

            if selected_option == Menues_option.SHOW:show_all_cars()
            elif selected_option == Menues_option.ADD:add_customers()
            elif selected_option == Menues_option.DELETE:delete_car()
            elif selected_option == Menues_option.EDIT:update_cars()
            elif selected_option == Menues_option.SEARCH_CAR:search_car_brand()
            elif selected_option == Menues_option.SEARCH_Customers:search_Customers()
            elif selected_option == Menues_option.EXIT:
                print("Goodbye!")
                exit()
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    # create_tables(cur)
    menu()
