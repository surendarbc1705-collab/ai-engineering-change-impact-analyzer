import sqlite3


def get_database_schema():

    connection = sqlite3.connect("customer.db")
    cursor = connection.cursor()

    tables = cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """).fetchall()

    schema = {}

    for table in tables:

        table_name = table[0]

        columns = cursor.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()

        schema[table_name] = [
            {
                "column": column[1],
                "type": column[2]
            }
            for column in columns
        ]

    connection.close()

    return schema