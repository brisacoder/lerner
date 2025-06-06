"""
examples_using_sqlalchemy_utils.py

Demonstrates usage of:
1. sqlalchemy_df_utils.py - DataFrame-based SQL operations
2. sqlalchemy_manual_utils.py - Core SQLAlchemy-based SQL operations

All operations are encapsulated in functions, PEP8-compliant, and include docstrings.
"""

import pandas as pd
from sqlalchemy import Column, Integer, String
import sqlalchemy_df_utils as df_utils
import sqlalchemy_manual_utils as core_utils


# ---------- Configuration ----------
USER = "your_user"
PASSWORD = "your_password"
HOST = "localhost"
DB = "your_database"
PORT = 3306


def run_dataframe_examples(engine):
    """
    Run operations using the dataframe-based utility module.
    """
    print("\n--- DataFrame-Based Operations ---")

    # Create initial DataFrame
    df = pd.DataFrame({
        "id": [1, 2],
        "name": ["Alice", "Bob"],
        "email": ["alice@example.com", "bob@example.com"]
    })

    # Create table
    df_utils.create_table_from_dataframe(engine, df, "users_df", if_exists="replace")

    # Insert more rows
    new_rows = pd.DataFrame({
        "id": [3],
        "name": ["Charlie"],
        "email": ["charlie@example.com"]
    })
    df_utils.insert_rows_from_dataframe(engine, new_rows, "users_df")

    # Update a row
    updates = pd.DataFrame({
        "id": [2],
        "name": ["Bobby"],
        "email": ["bobby@example.com"]
    })
    df_utils.update_rows_from_dataframe(engine, updates, "users_df", match_on=["id"])

    # Update a single cell
    df_utils.update_cell(engine, "users_df", {"id": 3}, "email", "new_charlie@example.com")

    # Fetch table as DataFrame
    df_fetched = df_utils.fetch_table_as_dataframe(engine, "users_df")
    print(df_fetched)

    # Delete row
    df_utils.delete_rows(engine, "users_df", {"id": 1})

    # Add new column
    df_utils.add_column(engine, "users_df", "status", "VARCHAR(20)")

    # Drop table
    df_utils.drop_table(engine, "users_df")


def run_core_examples(engine):
    """
    Run operations using the SQLAlchemy Core-based utility module.
    """
    print("\n--- Core-Based Operations ---")

    # Define schema
    columns = [
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("email", String(100))
    ]

    # Create table
    core_utils.create_table(engine, "users_core", columns)

    # Insert single row
    core_utils.insert_row(engine, "users_core", {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    })

    # Insert multiple rows
    core_utils.insert_rows(engine, "users_core", [
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ])

    # Update a row
    core_utils.update_row(engine, "users_core", {"id": 2}, {"email": "bobby@example.com"})

    # Delete a row
    core_utils.delete_rows(engine, "users_core", {"id": 1})

    # Fetch and display rows
    rows = core_utils.fetch_rows(engine, "users_core")
    for row in rows:
        print(row)

    # Drop table
    core_utils.drop_table(engine, "users_core")


def main():
    """
    Main driver function for running all examples.
    """
    engine = df_utils.get_engine(USER, PASSWORD, HOST, DB, PORT)
    run_dataframe_examples(engine)
    run_core_examples(engine)


if __name__ == "__main__":
    main()
