import re
import sqlite3
import pandas as pd
import tempfile
import os


Support_ext = [".csv", ".xlsx", ".xls", ".json", ".db", ".sqlite", ".sqlite3"]
Max_File_Size = 20


def load_file(uploaded_file) -> dict:
    """
    Takes a Streamlit uploaded file.
    Converts it to SQLite and returns metadata.
    """

    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()

    # ── Validate ──
    if ext not in Support_ext:
        raise ValueError(f"Unsupported file type: {ext}")

    if uploaded_file.size / (1024 * 1024) > Max_File_Size:
        raise ValueError(f"File too large. Maximum size is {Max_File_Size}MB")

    # ── Read into DataFrame ──
    if ext == ".csv":
        df = pd.read_csv(uploaded_file)

    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(uploaded_file)

    elif ext == ".json":
        df = pd.read_json(uploaded_file)

    elif ext in [".db", ".sqlite", ".sqlite3"]:
        # Save to temp file first then read
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        conn = sqlite3.connect(tmp_path)
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        df = pd.read_sql(f"SELECT * FROM {tables.iloc[0]['name']}", conn)
        conn.close()
        os.unlink(tmp_path)

    if df.empty:
        raise ValueError("The uploaded file is empty.")

    # ── Clean column names ──
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )

    # ── Get table name from filename ──
    table_name = os.path.splitext(filename)[0].lower().replace(" ", "_")
    table_name = re.sub(r"[^\w]", "", table_name) 

    # ── Save to temp SQLite ──
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = tmp.name
    tmp.close()

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    # ── Schema for prompt ──
    schema_lines = []
    for col, dtype in df.dtypes.items():
        if "int" in str(dtype):
            readable = "INTEGER"
        elif "float" in str(dtype):
            readable = "DECIMAL"
        elif "datetime" in str(dtype):
            readable = "DATE"
        else:
            readable = "TEXT"
        schema_lines.append(f"  - {col} ({readable})")

    return {
        "db_path": db_path,
        "table_name": table_name,
        "schema": "\n".join(schema_lines),
        "sample_rows": df.head(3).to_string(index=False),
        "row_count": len(df),
        "col_count": len(df.columns),
        "columns": list(df.columns)
    }


def load_demo_file(filepath):
    
    filename = filepath.split("/")[-1]
    
    df = pd.read_csv(filepath)
    
    table_name = os.path.splitext(filename)[0].lower().replace(" ", "_")
    table_name = re.sub(r"[^\w]", "", table_name) 
    
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = tmp.name
    tmp.close()
    
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    
    schema_lines = []
    for col, dtype in df.dtypes.items():
        if "int" in str(dtype): readable = "INTEGER"
        elif "float" in str(dtype): readable = "DECIMAL"
        elif "datetime" in str(dtype): readable = "DATE"
        else: readable = "TEXT"
        schema_lines.append(f"  - {col} ({readable})")

    return {
        "db_path": db_path,
        "table_name": table_name,
        "schema": "\n".join(schema_lines),
        "sample_rows": df.head(3).to_string(index=False),
        "row_count": len(df),
        "col_count": len(df.columns),
        "columns": list(df.columns)
    }