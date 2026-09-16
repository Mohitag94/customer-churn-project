"""
One-time setup: generates DuckDB schema from the train raw data csv file,
writes to sql/00_schema.sql, creates the table and loads the data.

Run: uv run python Src/load_data.py
"""

# load required packages...
import duckdb
import pandas as pd

from config import Columns, Paths

# dict for sql columns mapping
DTYPE_MAP = {
    "int64": "INTEGER",
    "float64": "DOUBLE",
    "object": "VARCHAR",
    "bool": "BOOLEAN",
}


def sql_table_build(df: pd.DataFrame) -> str:
    """
    Generates a CREATE TABLE query statement through mapping
    the dataframe column dtype to DUCKDB sql type ands put the
    primary key marked PRIMARY_KEY in the table under a schema-churn.

    Args:
                df: DataFrame whose column names and dtypes will define the table schema.

    Returns:
                A complete SQL string ready to execute (CREATE TABLE).
    """

    columns_sql = []
    for col, dtype in df.dtypes.items():
        col_sql_type = DTYPE_MAP.get(str(dtype), "VARCHAR")
        if col == Columns.PRIMARY_KEY:
            columns_sql.append(f"{col} VARCHAR PRIMARY KEY")
        else:
            columns_sql.append(f"{col} {col_sql_type}")

    # assumation: schema churn exists.
    table_query = "CREATE TABLE IF NOT EXISTS churn.train_customers (\n "
    table_query += ",\n".join(columns_sql) + "\n)"

    return table_query


def main():
    """
    Run the one-time schema generation and data load.

    Steps:
                1. Load the raw CSV into a DataFrame.
                2. Generate table SQL from the DataFrame's dtypes.
                3. Write the schema SQL to Paths.SCHEMA_FILE for version control/reference.
                4. Connect to the DuckDB database file, execute the schema, and insert the data.
                5. Print the resulting row count as a sainty check.
    """

    # load data
    df = pd.read_csv(Paths.RAW_CSV)

    table_query = sql_table_build(df)

    # write the buleprint to file
    with open(Paths.SCHEMA_FILE, "w") as f:
        f.write(table_query)
    print(f"[INFO] Schema written to {Paths.SCHEMA_FILE}")

    # database operations...
    con = duckdb.connect(Paths.DB_FILE)
    # create schema
    con.execute("CREATE SCHEMA IF NOT EXISTS churn;")
    # create table
    con.execute(table_query)
    # insert the contents
    con.execute(f"""
	INSERT INTO churn.train_customers 
	SELECT * FROM df
	ON CONFLICT ({Columns.PRIMARY_KEY}) DO NOTHING
	""")

    # count the number of inserts
    row_count = con.execute("SELECT COUNT(*) FROM churn.train_customers").fetchone()[0]
    print(f"[INFO] Number of inserted rows: {row_count}")

    con.close()


if __name__ == "__main__":
    main()
