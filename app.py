from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PRODUCTOS = 'inventario.db'
DB_CLIENTES = 'clientes.db'

# ---------------- INICIALIZACIÓN ---------------- #

def init_db_productos():
    if not os.path.exists(DB_PRODUCTOS):
        conn = sqlite3.connect(DB_PRODUCTOS)
        conn.execute("""
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                precio REAL,
                cantidad INTEGER
            )
        """)
        conn.commit()
        conn.close()

def init_db_clientes():
    if not os.path.exists(DB_CLIENTES):
        conn = sqlite3.connect(DB_CLIENTES)
        conn.execute("""
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_compra TEXT,
                nombre TEXT,
                celular TEXT,
                domicilio TEXT,
                producto TEXT,
                cuotas_totales INTEGER,
                cuotas_pagadas INTEGER,
                estado_deuda TEXT
            )
        """)
        conn.commit()
        conn.close()

init_db_productos()
init_db_clientes()

# ---------------- CONEXIONES ---------------- #

def get_productos_connection():
    conn = sqlite3.connect(DB_PRODUCTOS)
    conn.row_factory = sqlite3.Row
    return conn

def get_clientes_connection():
    conn = sqlite3.connect(DB_CLIENTES)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- RUTAS PRODUCTOS ---------------- #

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/productos')
def productos():
    conn = get_productos_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    cantidad = int(request.form['cantidad'])
    conn = get_productos_connection()
    conn.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)", (nombre, precio, cantidad))
    conn.commit()
    conn.close()
    return redirect('/productos')

# ---------------- RUTAS CLIENTES ---------------- #

@app.route('/clientes')
def clientes():
    conn = get_clientes_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    data = (
        request.form['fecha_compra'],
        request.form['nombre'],
        request.form['celular'],
        request.form['domicilio'],
        request.form['producto'],
        int(request.form['cuotas_totales']),
        int(request.form['cuotas_pagadas']),
        request.form['estado_deuda']
    )
    conn = get_clientes_connection()
    conn.execute("""
        INSERT INTO clientes (
            fecha_compra, nombre, celular, domicilio,
            producto, cuotas_totales, cuotas_pagadas, estado_deuda
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()
    return redirect('/clientes')

if __name__ == '__main__':
    app.run(debug=True)

