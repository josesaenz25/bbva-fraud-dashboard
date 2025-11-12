import sqlite3
import pandas as pd
from datetime import datetime

def crear_tabla():
    conn = sqlite3.connect("data/fraudes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            hour INTEGER,
            es_fraude INTEGER,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_transaccion(amount, hour, es_fraude):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("data/fraudes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transacciones (amount, hour, es_fraude, fecha) VALUES (?, ?, ?, ?)",
                   (amount, hour, es_fraude, fecha))
    conn.commit()
    conn.close()

def obtener_historial():
    conn = sqlite3.connect("data/fraudes.db")
    df = pd.read_sql_query("SELECT * FROM transacciones ORDER BY id DESC", conn)
    conn.close()
    return df
