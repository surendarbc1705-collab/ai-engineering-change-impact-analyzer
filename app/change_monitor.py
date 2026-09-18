import sqlite3

DB_PATH = "customer.db"


def get_customers():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    rows = cursor.execute("""
        SELECT
            Customer_ID,
            Customer_Name,
            Email,
            Customer_Status
        FROM Customer
        ORDER BY Customer_ID
    """).fetchall()

    connection.close()

    return rows


def detect_changes(before, after):
    changes = []

    before_data = {
        row[0]: row
        for row in before
    }

    after_data = {
        row[0]: row
        for row in after
    }

    # Check deleted and updated customers
    for customer_id in before_data:

        if customer_id not in after_data:
            changes.append({
                "type": "DELETED",
                "customer_id": customer_id,
                "before": before_data[customer_id],
                "after": None
            })
            continue

        old = before_data[customer_id]
        new = after_data[customer_id]

        column_names = [
            "Customer_ID",
            "Customer_Name",
            "Email",
            "Customer_Status"
        ]

        for index, column in enumerate(column_names):

            if old[index] != new[index]:
                changes.append({
                    "type": "UPDATED",
                    "customer_id": customer_id,
                    "column": column,
                    "old_value": old[index],
                    "new_value": new[index]
                })

    # Check newly added customers
    for customer_id in after_data:

        if customer_id not in before_data:
            changes.append({
                "type": "ADDED",
                "customer_id": customer_id,
                "before": None,
                "after": after_data[customer_id]
            })

    return changes