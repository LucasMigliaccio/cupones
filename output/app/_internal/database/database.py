import sqlite3
import os
import pandas as pd

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), "cupon.sqlite3")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"No se encontró el archivo de base de datos en {db_path}")
    conn = sqlite3.connect(db_path)
    return conn

def check_table_exists(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    cursor.execute(query)
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def create_tables_if_not_exists():
    conn = get_connection()
    cursor = conn.cursor()
    if not check_table_exists("cupones"):
        cursor.execute("""
    CREATE TABLE "cupon" (
	"ID"	INTEGER NOT NULL,
	"Artículo"	TEXT,
	"Nombre"	TEXT,
	"Física disponíble"	INTEGER,
	"Almacen"	INTEGER,
	"Clase"	TEXT,
	"Marca"	TEXT,
	"Matriz"	TEXT,
	"Tipo de Producto"	TEXT,
	"Precio anterior"	INTEGER,
	"Precio actual"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT)
    );
        """)
    conn.commit()
    conn.close()

def select_all():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM cupon;"
    cursor.execute(query)
    cupones = cursor.fetchall()
    conn.close()
    return cupones

def return_dataframe():
    conn = get_connection()
    query = "SELECT * FROM cupon;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df 

def delete_all():
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM cupon;"
    cursor.execute(query)
    conn.commit()
    conn.close()
    print ("tabla eliminada")
