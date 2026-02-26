import sqlite3
import pandas as pd

def read_query(db_path: str, query: str) -> pd.DataFrame:
    """
    Executes a SQL query on the specified SQLite database and returns the results as a DataFrame.
    """

    # Checking if the query is a SELECT statement
    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")
    
    # Connect to the SQLite database in only read mode
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)

    try:
        # Execute the query and fetch results into a DataFrame
        return pd.read_sql_query(query, conn)
    except Exception as e:
         raise ValueError(f"We could not run this query on your data. Please try rephrasing your question. Details: {str(e)}")

    finally:
        conn.close()
        


