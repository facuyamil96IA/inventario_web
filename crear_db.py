import sqlite3

conn = sqlite3.connect('inventario.db')
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        cantidad INTEGER
    )
""")
conn.commit()
conn.close()
print("Base de datos creada.")