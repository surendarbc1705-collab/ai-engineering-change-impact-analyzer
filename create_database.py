import sqlite3


# Connect to SQLite database
connection = sqlite3.connect("customer.db")
cursor = connection.cursor()


# ---------------------------------------
# Customer table
# ---------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    Customer_ID INTEGER PRIMARY KEY,
    Customer_Name TEXT NOT NULL,
    Email TEXT,
    Customer_Status TEXT,
    Customer_Type TEXT,
    Created_Date TEXT
)
""")


# ---------------------------------------
# Orders table
# ---------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    Order_ID INTEGER PRIMARY KEY,
    Customer_ID INTEGER,
    Order_Amount REAL,
    Order_Status TEXT,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
)
""")


# ---------------------------------------
# Customer Address table
# ---------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer_Address (
    Address_ID INTEGER PRIMARY KEY,
    Customer_ID INTEGER,
    City TEXT,
    Country TEXT,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
)
""")


# ---------------------------------------
# Clear existing demo data
# ---------------------------------------

cursor.execute("DELETE FROM Customer")
cursor.execute("DELETE FROM Orders")
cursor.execute("DELETE FROM Customer_Address")


# ---------------------------------------
# Insert customers
# ---------------------------------------

customers = [
    (
        1234567,
        "Surendar V",
        "surendarbc1705@gmail.com",
        "Working",
        "Premium",
        "2026-09-18"
    ),
    (
        1234545,
        "Sharmi T",
        "Sharmi@123gmail.com",
        "Working",
        "Standard",
        "2026-09-18"
    ),
    (
        1234534,
        "Arun G",
        "arun.123@gmail.com",
        "Working",
        "Standard",
        "2026-09-18"
    ),
    (
        2321345,
        "Ravi K",
        "ravimba@gmail.com",
        "Not working",
        "Standard",
        "2026-09-18"
    )
]


cursor.executemany("""
INSERT INTO Customer
(
    Customer_ID,
    Customer_Name,
    Email,
    Customer_Status,
    Customer_Type,
    Created_Date
)
VALUES (?, ?, ?, ?, ?, ?)
""", customers)


# ---------------------------------------
# Insert sample orders
# ---------------------------------------

orders = [
    (1001, 1234567, 2500.00, "Completed"),
    (1002, 1234545, 1200.00, "Pending"),
    (1003, 1234534, 4500.00, "Completed"),
    (1004, 2321345, 1800.00, "Pending")
]


cursor.executemany("""
INSERT INTO Orders
(
    Order_ID,
    Customer_ID,
    Order_Amount,
    Order_Status
)
VALUES (?, ?, ?, ?)
""", orders)


# ---------------------------------------
# Insert sample addresses
# ---------------------------------------

addresses = [
    (1, 1234567, "Chennai", "India"),
    (2, 1234545, "Coimbatore", "India"),
    (3, 1234534, "Bangalore", "India"),
    (4, 2321345, "Madurai", "India")
]


cursor.executemany("""
INSERT INTO Customer_Address
(
    Address_ID,
    Customer_ID,
    City,
    Country
)
VALUES (?, ?, ?, ?)
""", addresses)


# ---------------------------------------
# Save changes
# ---------------------------------------

connection.commit()
connection.close()


print("Customer database updated successfully!")
print("4 customer records added.")