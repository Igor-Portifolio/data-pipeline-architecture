import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path("C:/projetos_solve/scripts_geral/data/store/memory.db")

conn = sqlite3.connect(db_path)

# listar tabelas
print(pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
))

# inspecionar dados
df = pd.read_sql("SELECT * FROM IBGE LIMIT 10;", conn)
print(df)

conn.close()
