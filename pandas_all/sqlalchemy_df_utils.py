import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, text, update, delete
from sqlalchemy.exc import SQLAlchemyError


# ---------- Engine Helper ----------
def get_engine(user, password, host, db, port=3306):
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}")


# ---------- Table Creation ----------
def create_table_from_dataframe(
    engine, df: pd.DataFrame, table_name: str, if_exists="replace"
):
    df.to_sql(table_name, con=engine, index=False, if_exists=if_exists)
    print(f"✅ Table `{table_name}` created with {len(df)} rows.")


# ---------- Row Insertion ----------
def insert_rows_from_dataframe(engine, df: pd.DataFrame, table_name: str):
    df.to_sql(table_name, con=engine, index=False, if_exists="append")
    print(f"➕ Inserted {len(df)} row(s) into `{table_name}`.")


# ---------- Row Update ----------
def update_rows_from_dataframe(
    engine, df: pd.DataFrame, table_name: str, match_on: list[str]
):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    with engine.begin() as conn:
        for _, row in df.iterrows():
            filters = [table.c[k] == row[k] for k in match_on]
            values = {col: row[col] for col in df.columns if col not in match_on}
            stmt = update(table).where(*filters).values(**values)
            conn.execute(stmt)
    print(f"✏️ Updated {len(df)} row(s) in `{table_name}`.")


# ---------- Cell Update ----------
def update_cell(engine, table_name: str, row_filter: dict, column_name: str, new_value):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    with engine.begin() as conn:
        stmt = (
            update(table)
            .where(*[table.c[k] == v for k, v in row_filter.items()])
            .values({column_name: new_value})
        )
        conn.execute(stmt)
    print(
        f"✏️ Updated `{column_name}` to `{new_value}` where {row_filter} in `{table_name}`."
    )


# ---------- Row Deletion ----------
def delete_rows(engine, table_name: str, condition: dict):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    with engine.begin() as conn:
        stmt = delete(table).where(*[table.c[k] == v for k, v in condition.items()])
        result = conn.execute(stmt)
    print(f"➖ Deleted {result.rowcount} row(s) from `{table_name}`.")


# ---------- Add Column ----------
def add_column(
    engine, table_name: str, column_name: str, column_type: str = "VARCHAR(255)"
):
    with engine.begin() as conn:
        stmt = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        conn.execute(stmt)
    print(f"📐 Added column `{column_name}` to `{table_name}`.")


# ---------- Drop Table ----------
def drop_table(engine, table_name: str):
    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
    print(f"🧽 Dropped table `{table_name}`.")
