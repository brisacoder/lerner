import datetime
import os
import json
from decimal import Decimal
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import errorcode

import pandas as pd


# --------------------------------------------------------------------------------
# 1.  CONNECTION HANDLING
# --------------------------------------------------------------------------------


def get_connection(host: str | None, user: str | None, password: str | None):
    """
    Establish and return a MySQL connection.
    Replace the arguments with your own credentials.
    """
    if not host or not user or not password:
        raise ValueError("Host, user, and password must be provided.") 

    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=password, charset="utf8mb4", use_unicode=True
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌  Access denied: check your username/password")
        else:
            print(err)
        raise


# --------------------------------------------------------------------------------
# 2.  CREATE A TABLE WITH “ALL” SQL DATA TYPES
# --------------------------------------------------------------------------------


def create_example_table(conn):
    """
    Drop existing table (if any) and create a new one with
    columns spanning almost every common MySQL data type.
    """
    table_name = "pandas_mysql_example"

    ddl = f"""
    DROP TABLE IF EXISTS {table_name};
    CREATE TABLE {table_name} (
        id               INT             PRIMARY KEY AUTO_INCREMENT,
        small_int_col    SMALLINT,
        tiny_int_col     TINYINT,
        medium_int_col   MEDIUMINT,
        big_int_col      BIGINT,
        float_col        FLOAT,
        double_col       DOUBLE,
        decimal_col      DECIMAL(10,2),
        bit_col          BIT(1),
        char_col         CHAR(10),
        varchar_col      VARCHAR(255),
        binary_col       BINARY(16),
        varbinary_col    VARBINARY(255),
        blob_col         BLOB,
        text_col         TEXT,
        date_col         DATE,
        datetime_col     DATETIME,
        timestamp_col    TIMESTAMP NULL DEFAULT NULL,
        time_col         TIME,
        year_col         YEAR,
        enum_col         ENUM('value1','value2','value3'),
        set_col          SET('a','b','c'),
        json_col         JSON
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor = conn.cursor()
    # MySQL client allows multiple statements only if multi=True
    for result in cursor.execute(ddl, multi=True):
        pass
    conn.commit()
    cursor.close()
    print(f"✅  Table `{table_name}` created (or re-created).")


# --------------------------------------------------------------------------------
# 3.  INSERT A DATAFRAME INTO MYSQL (INSERT / ADD)
# --------------------------------------------------------------------------------


def insert_dataframe(conn, df: pd.DataFrame, table_name: str = "pandas_mysql_example"):
    """
    Given a DataFrame whose columns exactly match the non-auto-increment
    columns of the table, insert all rows into MySQL using executemany().
    """
    # List of columns in the same order as the CREATE TABLE, excluding 'id'
    columns = [
        "small_int_col",
        "tiny_int_col",
        "medium_int_col",
        "big_int_col",
        "float_col",
        "double_col",
        "decimal_col",
        "bit_col",
        "char_col",
        "varchar_col",
        "binary_col",
        "varbinary_col",
        "blob_col",
        "text_col",
        "date_col",
        "datetime_col",
        "timestamp_col",
        "time_col",
        "year_col",
        "enum_col",
        "set_col",
        "json_col",
    ]

    # Build the INSERT statement with placeholders
    cols_joined = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"INSERT INTO {table_name} ({cols_joined}) VALUES ({placeholders})"

    # Prepare the data as a list of tuples, in the same column order
    data_to_insert = []
    for idx, row in df.iterrows():
        tup = tuple(row[col] for col in columns)
        data_to_insert.append(tup)

    cursor = conn.cursor()
    cursor.executemany(insert_sql, data_to_insert)
    conn.commit()
    cursor.close()
    print(f"✅  Inserted {len(data_to_insert)} row(s) into `{table_name}`.")


# --------------------------------------------------------------------------------
# 4.  RETRIEVE DATA INTO A PANDAS DATAFRAME (SELECT / RETRIEVE)
# --------------------------------------------------------------------------------


def retrieve_to_dataframe(
    conn, table_name: str = "pandas_mysql_example"
) -> pd.DataFrame:
    """
    Run a simple SELECT * query and return the results as a Pandas DataFrame.
    """
    query = f"SELECT * FROM {table_name}"
    # pandas.read_sql can take a raw MySQLConnection from mysql.connector
    df = pd.read_sql(query, conn)
    print(f"🔍  Retrieved {len(df)} row(s) from `{table_name}`.")
    return df


# --------------------------------------------------------------------------------
# 5.  UPDATE EXISTING ROWS BASED ON A DATAFRAME (MODIFY)
# --------------------------------------------------------------------------------


def update_from_dataframe(
    conn, df: pd.DataFrame, table_name: str = "pandas_mysql_example"
):
    """
    Given a DataFrame that contains an 'id' column (primary key) plus
    all other columns, UPDATE each row in the table to match the DataFrame.
    """
    # All columns except 'id' in the same order as before
    columns = [
        "small_int_col",
        "tiny_int_col",
        "medium_int_col",
        "big_int_col",
        "float_col",
        "double_col",
        "decimal_col",
        "bit_col",
        "char_col",
        "varchar_col",
        "binary_col",
        "varbinary_col",
        "blob_col",
        "text_col",
        "date_col",
        "datetime_col",
        "timestamp_col",
        "time_col",
        "year_col",
        "enum_col",
        "set_col",
        "json_col",
    ]

    # Build SET clause: "col1 = %s, col2 = %s, ..."
    set_clause = ", ".join([f"{col} = %s" for col in columns])
    update_sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"

    cursor = conn.cursor()
    update_count = 0
    for idx, row in df.iterrows():
        # Build the parameter tuple: values in column order, then id last
        params = tuple(row[col] for col in columns) + (int(row["id"]),)
        cursor.execute(update_sql, params)
        update_count += cursor.rowcount

    conn.commit()
    cursor.close()
    print(f"✏️  Updated {update_count} row(s) in `{table_name}`.")


# --------------------------------------------------------------------------------
# 6.  DELETE ROWS BY ID (DELETE)
# --------------------------------------------------------------------------------


def delete_by_ids(conn, id_list, table_name: str = "pandas_mysql_example"):
    """
    Delete all rows whose 'id' is in id_list.
    id_list should be an iterable of integers.
    """
    cursor = conn.cursor()
    delete_sql = f"DELETE FROM {table_name} WHERE id = %s"
    data = [(int(_id),) for _id in id_list]
    cursor.executemany(delete_sql, data)
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    print(f"🗑️  Deleted {deleted} row(s) from `{table_name}` (ids: {id_list}).")


# --------------------------------------------------------------------------------
# 7.  EXAMPLE USAGE
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    load_dotenv(override=True)
    # ‣ Adjust these parameters to match your local MySQL server:
    HOST = "localhost"
    USER = os.getenv("MYSQL_USERNAME")
    PASSWORD = os.getenv("MYSQL_PASSWORD")
    DATABASE = "your_database"

    # (A)  Establish the connection
    conn = get_connection(HOST, USER, PASSWORD)

    # (B)  Re-create the example table
    create_example_table(conn)

    # (C)  Build a DataFrame with exactly one row, showing how each SQL type maps
    example_row = {
        "small_int_col": 123,  # SMALLINT  → int
        "tiny_int_col": 1,  # TINYINT   → int (used for BOOL, etc.)
        "medium_int_col": 1000,  # MEDIUMINT → int
        "big_int_col": 1234567890123,  # BIGINT    → int
        "float_col": 1.23,  # FLOAT     → float
        "double_col": 3.1415926535,  # DOUBLE    → float
        "decimal_col": Decimal("12345.67"),  # DECIMAL   → Decimal (or object in Pandas)
        "bit_col": 1,  # BIT(1)    → int (0 or 1)
        "char_col": "char_data",  # CHAR(10)  → str
        "varchar_col": "varchar data example",  # VARCHAR   → str
        # BINARY(16) requires exactly 16 bytes; we pad/truncate to length 16
        "binary_col": b"bin_data_123456",  # BINARY   → bytes
        "varbinary_col": b"varbinary data here",  # VARBINARY→ bytes
        "blob_col": b"\x00\x01\x02\x03",  # BLOB     → bytes
        "text_col": "This is a TEXT column with a longer string.",  # TEXT → str
        "date_col": datetime.date(2025, 6, 4),  # DATE     → datetime.date
        "datetime_col": datetime.datetime(2025, 6, 4, 15, 30, 0),  # DATETIME→ datetime
        "timestamp_col": datetime.datetime(
            2025, 6, 4, 15, 30, 0
        ),  # TIMESTAMP → datetime
        "time_col": datetime.time(15, 30, 0),  # TIME    → datetime.time
        "year_col": 2025,  # YEAR    → int
        "enum_col": "value2",  # ENUM    → str
        "set_col": "a,c",  # SET     → str (comma-separated)
        # JSON column expects a valid JSON string
        "json_col": json.dumps({"key": "value", "number": 123}),
    }

    # Create DataFrame with one row
    df_initial = pd.DataFrame([example_row])

    # (D)  Insert the DataFrame into MySQL
    insert_dataframe(conn, df_initial)

    # (E)  Retrieve the table back into Pandas to confirm the insert
    df_retrieved = retrieve_to_dataframe(conn)
    print("\n>>> DataFrame after INSERT:\n", df_retrieved, "\n")

    # (F)  MODIFY: let's change the varchar_col of id=1, and also tweak a numeric
    #      We operate on df_retrieved, then write those changes back.
    if not df_retrieved.empty:
        df_modified = df_retrieved.copy()
        # Assume 'id' = 1 exists
        df_modified.loc[df_modified["id"] == 1, "varchar_col"] = "updated varchar!"
        df_modified.loc[df_modified["id"] == 1, "float_col"] = 9.87

        update_from_dataframe(conn, df_modified)

        # Retrieve again to see the updates
        df_after_update = retrieve_to_dataframe(conn)
        print("\n>>> DataFrame after UPDATE:\n", df_after_update, "\n")

    # (G)  DELETE: delete the row with id=1
    ids_to_delete = df_retrieved["id"].tolist()
    if ids_to_delete:
        delete_by_ids(conn, ids_to_delete)

        # Final retrieval to confirm deletion
        df_final = retrieve_to_dataframe(conn)
        print("\n>>> DataFrame after DELETE:\n", df_final, "\n")

    # (H)  Close connection
    conn.close()
    print("🔒  Connection closed.")
