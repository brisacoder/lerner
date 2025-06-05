"""
sqlalchemy_df_utils.py

A utility module for performing common SQL operations with SQLAlchemy and Pandas
on a MySQL database. Supports creating tables from DataFrames, inserting,
updating, deleting, modifying cells, adding columns, and fetching results.

Author: rapenno
"""

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text, update, delete, inspect
from sqlalchemy.engine import Engine


def get_engine(user: str, password: str, host: str, db: str, port: int = 3306) -> Engine:
    """
    Create a SQLAlchemy engine for MySQL using mysql-connector.
    """
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}")


def create_table_from_dataframe(engine: Engine, df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> bool:
    """
    Create or replace a MySQL table using a DataFrame.
    """
    try:
        df.to_sql(table_name, con=engine, index=False, if_exists=if_exists)
        print(f"✅ Table `{table_name}` created with {len(df)} rows.")
        return True
    except Exception as e:
        print(f"❌ Failed to create table `{table_name}`: {e}")
        return False


def insert_rows_from_dataframe(engine: Engine, df: pd.DataFrame, table_name: str) -> int:
    """
    Insert rows from a DataFrame into an existing MySQL table.
    Returns the number of rows inserted.
    """
    try:
        df.to_sql(table_name, con=engine, index=False, if_exists='append')
        print(f"➕ Inserted {len(df)} row(s) into `{table_name}`.")
        return len(df)
    except Exception as e:
        print(f"❌ Failed to insert rows into `{table_name}`: {e}")
        return 0


def update_rows_from_dataframe(engine: Engine, df: pd.DataFrame, table_name: str, match_on: list[str]) -> int:
    """
    Update rows in a MySQL table using a DataFrame and match columns.
    Returns the number of rows attempted to update.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    updated = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            filters = [table.c[k] == row[k] for k in match_on]
            values = {col: row[col] for col in df.columns if col not in match_on}
            stmt = update(table).where(*filters).values(**values)
            result = conn.execute(stmt)
            updated += result.rowcount
    print(f"✏️ Updated {updated} row(s) in `{table_name}`.")
    return updated


def update_cell(engine: Engine, table_name: str, row_filter: dict, column_name: str, new_value) -> bool:
    """
    Update a single cell in a MySQL table.
    Returns True if the update affected any row.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    with engine.begin() as conn:
        stmt = update(table).where(
            *[table.c[k] == v for k, v in row_filter.items()]
        ).values({column_name: new_value})
        result = conn.execute(stmt)
        success = result.rowcount > 0

    if success:
        print(f"✏️ Updated `{column_name}` to `{new_value}` where {row_filter} in `{table_name}`.")
    else:
        print(f"⚠️ No rows matched for update in `{table_name}` with filter {row_filter}.")
    return success


def delete_rows(engine: Engine, table_name: str, condition: dict) -> int:
    """
    Delete rows from a MySQL table based on a condition.
    Returns the number of rows deleted.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    with engine.begin() as conn:
        stmt = delete(table).where(*[table.c[k] == v for k, v in condition.items()])
        result = conn.execute(stmt)
    print(f"➖ Deleted {result.rowcount} row(s) from `{table_name}`.")
    return result.rowcount


def add_column(engine: Engine, table_name: str, column_name: str, column_type: str = "VARCHAR(255)") -> bool:
    """
    Add a new column to an existing MySQL table.
    Returns True if successful.
    """
    try:
        with engine.begin() as conn:
            stmt = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            conn.execute(stmt)
        print(f"📐 Added column `{column_name}` to `{table_name}`.")
        return True
    except Exception as e:
        print(f"❌ Failed to add column `{column_name}` to `{table_name}`: {e}")
        return False


def drop_table(engine: Engine, table_name: str) -> bool:
    """
    Drop a table from the database if it exists.
    Returns True if the operation was successful.
    """
    try:
        with engine.begin() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        print(f"🧽 Dropped table `{table_name}`.")
        return True
    except Exception as e:
        print(f"❌ Failed to drop table `{table_name}`: {e}")
        return False


def fetch_table_as_dataframe(engine: Engine, table_name: str, columns: list[str] = None, where: str = None) -> pd.DataFrame:
    """
    Fetch table data from MySQL into a Pandas DataFrame.
    """
    try:
        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        df = pd.read_sql(query, engine)
        print(f"🔍 Retrieved {len(df)} row(s) from `{table_name}`.")
        return df
    except Exception as e:
        print(f"❌ Failed to fetch data from `{table_name}`: {e}")
        return pd.DataFrame()


def table_exists(engine: Engine, table_name: str) -> bool:
    """
    Check if a table exists in the connected MySQL database.
    """
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()
